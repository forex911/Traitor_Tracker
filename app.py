from flask import Flask, request, render_template, send_file
import os
import tempfile
import hashlib
import shutil
import time
import cv2
from datetime import datetime
from werkzeug.utils import secure_filename

from database.db import get_db_connection, init_db
from core.embed import embed_watermark
from core.extract import extract_watermark
from attacks.dispatcher import apply_attack
from security.keys import get_secret_key
from config.settings import ALLOWED_FORMATS

app = Flask(__name__)

# Initialize database tables if they do not exist
init_db()

if os.environ.get("VERCEL"):
    BASE_DIR = os.path.join(tempfile.gettempdir(), "traitor_tracer_samples")
else:
    BASE_DIR = os.environ.get("STORAGE_DIR", "samples")

# --------------------------------------------------
# CONSTANTS
# --------------------------------------------------
WATERMARK_LEN = 32
SIMILARITY_THRESHOLD = 0.75   # relaxed for attacked images
MAX_TEMP_AGE_SECONDS = 3600   # cleanup files older than 1 hour


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def similarity(a: str, b: str) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    return sum(x == y for x, y in zip(a, b)) / len(a)


def unique_folder(prefix: str) -> str:
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def allowed_file(filename: str) -> bool:
    """Check if the file extension is in the allowed list."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_FORMATS


def cleanup_old_files(directory: str, max_age: int = MAX_TEMP_AGE_SECONDS):
    """Remove subdirectories older than max_age seconds."""
    if not os.path.isdir(directory):
        return
    now = time.time()
    for entry in os.scandir(directory):
        if entry.is_dir():
            try:
                if now - entry.stat().st_mtime > max_age:
                    shutil.rmtree(entry.path, ignore_errors=True)
            except OSError:
                pass


# --------------------------------------------------
# HOME DASHBOARD
# --------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        active_section="watermark"
    )


# --------------------------------------------------
# EMBED WATERMARK
# --------------------------------------------------
@app.route("/upload", methods=["POST"])
def upload_image():
    user_id = request.form.get("user_id")
    image = request.files.get("image")

    if not user_id or not image:
        return render_template(
            "index.html",
            active_section="watermark",
            error="User ID and image are required"
        )

    # Validate filename and file type
    filename = secure_filename(image.filename)
    if not filename or not allowed_file(filename):
        return render_template(
            "index.html",
            active_section="watermark",
            error=f"Invalid file type. Allowed: {', '.join(ALLOWED_FORMATS)}"
        )

    folder = unique_folder(user_id)

    original_dir = os.path.join(BASE_DIR, "original", folder)
    watermarked_dir = os.path.join(BASE_DIR, "watermarked", folder)
    os.makedirs(original_dir, exist_ok=True)
    os.makedirs(watermarked_dir, exist_ok=True)

    input_path = os.path.join(original_dir, filename)
    output_path = os.path.join(watermarked_dir, filename)

    image.save(input_path)

    # Generate watermark
    secret = get_secret_key()
    watermark_text = hashlib.sha256(
        f"{secret}:{user_id}".encode()
    ).hexdigest()[:WATERMARK_LEN]

    # Embed watermark
    watermarked_img = embed_watermark(input_path, watermark_text)
    cv2.imwrite(output_path, watermarked_img)

    # Hash actual file bytes for content verification
    with open(input_path, "rb") as f:
        content_hash = hashlib.sha256(f.read()).hexdigest()

    # Store record
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO watermark_records (user_id, content_hash, watermark_key)
            VALUES (%s, %s, %s)
            """,
            (user_id, content_hash, watermark_text)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        pass  # DB may be unavailable; watermarked image is still returned

    return send_file(output_path, as_attachment=True)


# --------------------------------------------------
# TRACE IMAGE (NORMAL CHECK)
# --------------------------------------------------
@app.route("/trace-image", methods=["POST"])
def trace_image():
    image = request.files.get("image")

    if not image:
        return render_template(
            "index.html",
            active_section="checker",
            error="Please upload an image"
        )

    # Validate filename
    filename = secure_filename(image.filename)
    if not filename or not allowed_file(filename):
        return render_template(
            "index.html",
            active_section="checker",
            error=f"Invalid file type. Allowed: {', '.join(ALLOWED_FORMATS)}"
        )

    folder = unique_folder("CHECK")
    attacked_dir = os.path.join(BASE_DIR, "attacked", folder)
    os.makedirs(attacked_dir, exist_ok=True)

    image_path = os.path.join(attacked_dir, filename)
    image.save(image_path)

    try:
        extracted = extract_watermark(image_path, WATERMARK_LEN).strip()
    except Exception:
        extracted = ""

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, watermark_key, created_at FROM watermark_records"
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception:
        rows = []

    for user_id, stored_key, created_at in rows:
        score = similarity(extracted, stored_key)
        if score >= SIMILARITY_THRESHOLD:
            return render_template(
                "index.html",
                active_section="checker",
                result={
                    "user": user_id,
                    "time": str(created_at),
                    "score": f"{score * 100:.1f}%"
                }
            )

    return render_template(
        "index.html",
        active_section="checker",
        error="No matching watermark found"
    )


# --------------------------------------------------
# ATTACK DASHBOARD
# --------------------------------------------------
@app.route("/attack", methods=["GET"])
def attack_dashboard():
    # Cleanup old temp files on dashboard load
    for subdir in ("attacked", "trace"):
        cleanup_old_files(os.path.join(BASE_DIR, subdir))
    return render_template("attack.html")


# --------------------------------------------------
# RUN ATTACK(S) + EVALUATE
# --------------------------------------------------
@app.route("/attack-run", methods=["POST"])
def attack_run():
    image = request.files.get("image")
    attack_type = request.form.get("attack_type")

    if not image or not attack_type:
        return render_template(
            "attack.html",
            error="Image and attack type are required"
        )

    # Validate filename
    filename = secure_filename(image.filename)
    if not filename or not allowed_file(filename):
        return render_template(
            "attack.html",
            error=f"Invalid file type. Allowed: {', '.join(ALLOWED_FORMATS)}"
        )

    folder = unique_folder("ATTACK")
    base_dir = os.path.join(BASE_DIR, "trace", folder)
    os.makedirs(base_dir, exist_ok=True)

    original_path = os.path.join(base_dir, filename)
    image.save(original_path)

    # Fetch all watermark keys
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT watermark_key FROM watermark_records")
        keys = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
    except Exception:
        keys = []

    attack_result = apply_attack(original_path, attack_type)

    # ---------------- ALL ATTACK MODE ----------------
    if isinstance(attack_result, dict):
        results = []

        for attack, path in attack_result.items():
            try:
                extracted = extract_watermark(path, WATERMARK_LEN).strip()
            except Exception:
                extracted = ""

            best_score = 0.0
            for key in keys:
                best_score = max(best_score, similarity(extracted, key))

            results.append({
                "attack": attack,
                "extracted": extracted if extracted else "None",
                "score": f"{best_score * 100:.1f}%",
                "success": best_score >= SIMILARITY_THRESHOLD
            })

        return render_template(
            "attack.html",
            all_results=results
        )

    # ---------------- SINGLE ATTACK MODE ----------------
    try:
        extracted = extract_watermark(attack_result, WATERMARK_LEN).strip()
    except Exception:
        extracted = ""

    best_score = 0.0
    for key in keys:
        best_score = max(best_score, similarity(extracted, key))

    return render_template(
        "attack.html",
        result={
            "attack": attack_type,
            "extracted": extracted if extracted else "None",
            "score": f"{best_score * 100:.1f}%",
            "success": best_score >= SIMILARITY_THRESHOLD
        }
    )


# --------------------------------------------------
# SILENCE FAVICON ERROR
# --------------------------------------------------
@app.route("/favicon.ico")
def favicon():
    return "", 204


# --------------------------------------------------
# RUN APP
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)