import cv2
import os

from attacks.crop import run as run_crop
from attacks.resize import run as run_resize
from attacks.compress import run as run_compress
from attacks.noise import run as run_noise, gaussian_noise

from core.embed import embed_watermark
from core.detect import detect_watermark_energy

ORIGINAL = "samples/original/test.jpg"
WATERMARKED = "samples/watermarked/test.jpg"
ATTACKED_DIR = "samples/attacked"

WATERMARK_TEXT = "TRAITOR"

os.makedirs(ATTACKED_DIR, exist_ok=True)


def ensure_watermarked():
    if not os.path.exists(WATERMARKED):
        os.makedirs(os.path.dirname(WATERMARKED), exist_ok=True)
        wm = embed_watermark(ORIGINAL, WATERMARK_TEXT)
        cv2.imwrite(WATERMARKED, wm)


def assert_detected(path):
    assert detect_watermark_energy(path), "Watermark NOT detected"


def test_crop_attack():
    ensure_watermarked()

    out_path = run_crop(WATERMARKED)
    assert os.path.exists(out_path), "Cropped image not saved"
    assert_detected(out_path)


def test_resize_attack():
    ensure_watermarked()

    out_path = run_resize(WATERMARKED)
    assert os.path.exists(out_path), "Resized image not saved"
    assert_detected(out_path)


def test_compression_attack():
    ensure_watermarked()

    out_path = run_compress(WATERMARKED)
    assert os.path.exists(out_path), "Compressed image not saved"
    assert_detected(out_path)


def test_noise_attack():
    ensure_watermarked()

    out_path = run_noise(WATERMARKED)
    assert os.path.exists(out_path), "Noisy image not saved"
    assert_detected(out_path)


def test_gaussian_noise_direct():
    """Test the gaussian_noise function directly with an image array."""
    ensure_watermarked()
    img = cv2.imread(WATERMARKED)

    attacked = gaussian_noise(img, var=20)
    path = os.path.join(ATTACKED_DIR, "noise_direct.jpg")
    cv2.imwrite(path, attacked)

    assert_detected(path)

