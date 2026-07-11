import os

# Disable Numba JIT
os.environ["NUMBA_DISABLE_JIT"] = "1"

from flask import Flask, render_template, request, jsonify
import joblib
import subprocess
import imageio_ffmpeg

from utils import predict_parkinsons

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = joblib.load("Model/model.pkl")
scaler = joblib.load("Model/scaler.pkl")

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    try:

        if "audio" not in request.files:
            return jsonify({
                "success": False,
                "message": "No audio received."
            }), 400

        audio = request.files["audio"]

        webm_path = os.path.join(UPLOAD_FOLDER, "recording.webm")
        wav_path = os.path.join(UPLOAD_FOLDER, "recording.wav")

        audio.save(webm_path)

        print("Saved:", webm_path)

        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-i",
                webm_path,
                wav_path
            ],
            check=True
        )

        print("Converted:", wav_path)

        print("Starting Prediction...")

        result, confidence = predict_parkinsons(
            wav_path,
            model,
            scaler
        )

        print("Prediction:", result)
        print("Confidence:", confidence)

        return jsonify({
            "success": True,
            "prediction": result,
            "confidence": round(confidence, 2)
        })

    except subprocess.CalledProcessError as e:

        print("FFmpeg Error")
        print(e)

        return jsonify({
            "success": False,
            "message": "FFmpeg conversion failed."
        }), 500

    except Exception as e:

        print("Prediction Error")
        print(str(e))

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
