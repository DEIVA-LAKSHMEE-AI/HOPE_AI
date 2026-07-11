import os

# ==========================
# Numba cache — must be set BEFORE librosa/numba import,
# otherwise every worker/process recompiles from scratch.
# ==========================
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba_cache")
os.makedirs(os.environ["NUMBA_CACHE_DIR"], exist_ok=True)

import uuid
import subprocess
import numpy as np
import soundfile as sf
import joblib
import imageio_ffmpeg
from flask import Flask, render_template, request, jsonify

from utils import predict_parkinsons, extract_features

app = Flask(__name__)

# ==========================
# Upload Folder
# ==========================
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================
# Load Model
# ==========================
model = joblib.load("Model/model.pkl")
scaler = joblib.load("Model/scaler.pkl")

# FFmpeg executable
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()


# ==========================
# Warm up librosa/numba at boot
# ==========================
# First call to several librosa functions triggers a one-time numba
# JIT compile that can take 20-60s+ on a slow CPU. If that happens
# on a real user's request, gunicorn's timeout kills the worker.
# Doing it once here, at startup, moves that cost to deploy time.
def warmup():
    try:
        print("Warming up librosa/numba...")
        dummy = np.zeros(22050, dtype=np.float32)  # 1s of silence
        warmup_path = os.path.join(UPLOAD_FOLDER, "_warmup.wav")
        sf.write(warmup_path, dummy, 22050)
        extract_features(warmup_path)
        os.remove(warmup_path)
        print("Warmup complete.")
    except Exception as e:
        print("Warmup failed (non-fatal):", e)


warmup()


# ==========================
# Home
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Upload Audio
# ==========================
@app.route("/upload", methods=["POST"])
def upload():

    webm_path = None
    wav_path = None

    try:

        if "audio" not in request.files:
            return jsonify({
                "success": False,
                "message": "No audio received."
            }), 400

        audio = request.files["audio"]

        # Unique filenames per request so concurrent users don't
        # overwrite each other's recordings.
        request_id = uuid.uuid4().hex
        webm_path = os.path.join(UPLOAD_FOLDER, f"{request_id}.webm")
        wav_path = os.path.join(UPLOAD_FOLDER, f"{request_id}.wav")

        audio.save(webm_path)
        print("Saved:", webm_path)

        # Convert WebM -> WAV
        subprocess.run(
            [ffmpeg, "-y", "-i", webm_path, wav_path],
            check=True,
            capture_output=True,
        )
        print("Converted:", wav_path)

        # Predict
        result, confidence = predict_parkinsons(wav_path, model, scaler)

        return jsonify({
            "success": True,
            "prediction": result,
            "confidence": round(confidence, 2)
        })

    except subprocess.CalledProcessError as e:
        print("FFmpeg Error:", e.stderr)
        return jsonify({
            "success": False,
            "message": "FFmpeg conversion failed."
        }), 500

    except Exception as e:
        print("General Error:", e)
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        # Clean up temp files regardless of success/failure
        for p in (webm_path, wav_path):
            try:
                if p and os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass


# ==========================
# Run Flask (local dev only — Render uses gunicorn via Start Command)
# ==========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
