from flask import Flask, render_template, request, jsonify
import os
import joblib
import subprocess
import imageio_ffmpeg

from utils import predict_parkinsons

app = Flask(__name__)

# ==========================
# Upload Folder
# ==========================
UPLOAD_FOLDER = "Static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================
# Load Model
# ==========================
model = joblib.load("Model/model.pkl")
scaler = joblib.load("Model/scaler.pkl")

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

        if "audio" not in request.files:
            return jsonify({
                "success": False,
                "message": "No audio received."
            }), 400

        audio = request.files["audio"]

        webm_path = os.path.join(UPLOAD_FOLDER, "recording.webm")
        wav_path = os.path.join(UPLOAD_FOLDER, "recording.wav")

        # Save uploaded recording
        audio.save(webm_path)

        print("Saved:", webm_path)

        # Convert WebM -> WAV
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

        # Predict
        result, confidence = predict_parkinsons(
            wav_path,
            model,
            scaler
        )

        return jsonify({
            "success": True,
            "prediction": result,
            "confidence": round(confidence, 2)
        })

    except subprocess.CalledProcessError as e:

        print("FFmpeg Error:")
        print(e)

        return jsonify({
            "success": False,
            "message": "FFmpeg conversion failed."
        }), 500

    except Exception as e:

        print("General Error:")
        print(e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/dataset_test")
def dataset_test():

    file_path = r"D:\Projects\Parkinson_AI\Phase_1_ML_Model\Datasets\Voice_Dataset\Parkinsons\parkinsons_000.wav"

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