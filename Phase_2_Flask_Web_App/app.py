from flask import Flask, render_template, request, jsonify
import os
import joblib
import subprocess
import traceback
import imageio_ffmpeg

from utils import predict_parkinsons

app = Flask(__name__)

# ==========================
# Upload Folder
# ==========================
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================
# Load Model
# ==========================
print("Loading model...")
model = joblib.load("Model/model.pkl")

print("Loading scaler...")
scaler = joblib.load("Model/scaler.pkl")

print("Model loaded successfully.")

# FFmpeg executable
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()


# ==========================
# Home
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Test Route
# ==========================
@app.route("/test")
def test():

    file_path = "../Phase_1_ML_Model/Datasets/Voice_Dataset/Healthy/healthy_000.wav"

    print("Running test prediction...")

    result, confidence = predict_parkinsons(
        file_path,
        model,
        scaler
    )

    return f"""
    <h2>Prediction : {result}</h2>
    <h3>Confidence : {confidence:.2f}%</h3>
    """


# ==========================
# Upload Audio
# ==========================
@app.route("/upload", methods=["POST"])
def upload():

    try:

        print("========== NEW REQUEST ==========")

        if "audio" not in request.files:
            return jsonify({
                "success": False,
                "message": "No audio received."
            }), 400

        audio = request.files["audio"]

        webm_path = os.path.join(UPLOAD_FOLDER, "recording.webm")
        wav_path = os.path.join(UPLOAD_FOLDER, "recording.wav")

        print("Saving uploaded file...")

        audio.save(webm_path)

        print("Saved:", webm_path)

        print("Converting to wav...")

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

        print("Conversion completed.")

        print("Calling predict_parkinsons()...")

        result, confidence = predict_parkinsons(
            wav_path,
            model,
            scaler
        )

        print("Prediction completed.")

        return jsonify({
            "success": True,
            "prediction": result,
            "confidence": round(confidence, 2)
        })

    except subprocess.CalledProcessError as e:

        print("FFmpeg Error")
        traceback.print_exc()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    except Exception as e:

        print("GENERAL ERROR")
        traceback.print_exc()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================
# Dataset Test
# ==========================
@app.route("/dataset_test")
def dataset_test():

    file_path = "Model/test.wav"

    result, confidence = predict_parkinsons(
        file_path,
        model,
        scaler
    )

    return f"""
    <h2>Prediction: {result}</h2>
    <h3>Confidence: {confidence:.2f}%</h3>
    """


# ==========================
# Run Flask
# ==========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
