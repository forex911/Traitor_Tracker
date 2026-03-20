<h1 align="center">
  Traitor-Tracer 🕵️‍♂️
</h1>

<p align="center">
  <strong>Invisible Image Watermarking & Traitor Identification System</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/forex911/Traitor_Tracker?style=flat-square" alt="License" />
  <img src="https://img.shields.io/github/stars/forex911/Traitor_Tracker?style=flat-square" alt="Stars" />
  <img src="https://img.shields.io/github/forks/forex911/Traitor_Tracker?style=flat-square" alt="Forks" />
  <img src="https://img.shields.io/github/issues/forex911/Traitor_Tracker?style=flat-square" alt="Issues" />
</p>

<hr>

## 📖 Overview

**Traitor-Tracer** is a robust, web-based security system that embeds invisible watermarks into digital images, enabling seamless source tracking and traitor identification. Built with Python and Flask, the system not only embeds cryptographic identifiers but also evaluates the watermark's robustness under various real-world attacks.

Whether an image is cropped, resized, compressed, or injected with noise, Traitor-Tracer attempts to extract the embedded identity to trace the origin of unauthorized leaks.

---

## ✨ Key Features

- **🛡️ Invisible Watermarking:** Embeds unique user identifiers directly into the spatial/frequency domain of an image, imperceptible to the naked eye.
- **🔍 Traitor Identification:** Extracts the watermark from a suspected leaked image and matches it against the database to catch the culprit.
- **⚔️ Attack Evaluation:** Simulates real-world alterations to evaluate watermark robustness and survivability.
- **📊 Similarity Analysis:** Uses advanced similarity-based detection with interpretable failure analysis to judge watermark degradation.
- **🚀 Cloud-Ready:** Pre-configured for seamless deployments on modern platforms like **Vercel** and **Render**.
- **🧩 Modular Architecture:** Extensible design making it easy to plug in new watermarking algorithms or attack models.

---

## 🏗️ System Architecture

### 1. Watermark Embedding
- Accepts an original image and a unique user identifier.
- Generates a cryptographically secure hash to function as the watermark.
- Embeds the invisible watermark and stores the metadata securely in a PostgreSQL database.

### 2. Traitor Checker
- Takes in a potentially compromised/leaked image.
- Attempts to extract the residual watermark data.
- Cross-references the extracted data with the database.

### 3. Attack Evaluation Module
Evaluates watermark robustness by applying standard degradation attacks:

| Attack Type | Description |
| :--- | :--- |
| **Crop** | Removes a portion of the image to test partial recovery. |
| **Resize** | Scales the image resolution up or down. |
| **Noise** | Adds Gaussian noise to disrupt pixel-level data. |
| **Compress** | Applies heavy JPEG compression to filter out high-frequency details. |
| **All** | Runs all attacks sequentially to simulate worst-case scenarios. |

---

## 🛠️ Technology Stack

- **Backend:** Python, Flask, Gunicorn
- **Image Processing:** OpenCV, NumPy
- **Signal Processing:** SciPy, PyWavelets
- **Database:** PostgreSQL (via psycopg2)
- **Security:** Cryptography module
- **Frontend:** HTML5, CSS3, Jinja2 Templates

---

## 🚀 Installation & Setup

### Prerequisites
Make sure you have **Python 3.9+** and **PostgreSQL** installed.

### 1. Clone the repository
```bash
git clone https://github.com/forex911/Traitor_Tracker.git
cd Traitor_Tracker
```

### 2. Create a virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory for your database configuration:
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=traitor_tracker
```

### 5. Run the application locally
```bash
python app.py
```
*Access the application at: `http://127.0.0.1:5000`*

---

## ☁️ Deployment

**Traitor-Tracer** is configured for instant serverless/PaaS deployment. 

### Deploy to Vercel
1. Import the repository into your Vercel dashboard.
2. Vercel will automatically use the `vercel.json` file to configure the Python serverless environment.
3. Add your `DB_*` variables in the Vercel Settings, and add `VERCEL=1` to use the `/tmp` directory for ephemeral storage.

### Deploy to Render
1. Connect the repository to your Render dashboard.
2. Render will automatically detect the `render.yaml` configuration.
3. Provide the environment variables, and the app will start instantly via Gunicorn.

---

## 📈 Evaluation & Limitations

- **High Similarity:** Safely maintained for non-attacked images.
- **Noise Resilience:** Operates robustly under minor noise injections.
- **Geometric Vulnerability:** Shows degradation under severe geometric attacks (like aggressive cropping) – a well-known limitation of spatial-domain watermarking.

### Future Enhancements
- [ ] Implement Frequency-domain watermarking (DCT / DWT).
- [ ] Integrate Error-Correction Coding (ECC) for improved data recovery.
- [ ] Adaptive thresholding per attack type.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check out the [issues page](https://github.com/forex911/Traitor_Tracker/issues) to see what we're working on.

---

## 📝 License

This project is licensed under the **MIT License**.

> **Note:** This project is designed as an educational and research-oriented system. Observed failures under certain attacks are expected behavior and are clearly reported and analyzed for transparency.

<div align="center">
  <i>Copyright © forex911 · Built for Security and Accountability</i>
</div>