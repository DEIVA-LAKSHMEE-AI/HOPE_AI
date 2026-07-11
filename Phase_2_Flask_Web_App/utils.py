import os
import numpy as np
import librosa
import numpy as np
import librosa


# ==========================================================
# Load & Preprocess Audio
# ==========================================================
def load_audio(file_path):

    y, sr = librosa.load(
        file_path,
        sr=22050,
        mono=True
    )

    # Remove silence
    y, _ = librosa.effects.trim(
        y,
        top_db=20
    )

    # Normalize volume
    y = librosa.util.normalize(y)

    return y, sr


# ==========================================================
# Feature Extraction
# ==========================================================
def extract_features(file_path):

    y, sr = load_audio(file_path)

    # MFCC
    mfcc = np.mean(
        librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=40
        ).T,
        axis=0
    )

    # Chroma
    chroma = np.mean(
        librosa.feature.chroma_stft(
            y=y,
            sr=sr
        ).T,
        axis=0
    )

    # Mel Spectrogram
    mel = np.mean(
        librosa.feature.melspectrogram(
            y=y,
            sr=sr
        ).T,
        axis=0
    )

    # Spectral Contrast
    contrast = np.mean(
        librosa.feature.spectral_contrast(
            y=y,
            sr=sr
        ).T,
        axis=0
    )

    # Tonnetz
    harmonic = librosa.effects.harmonic(y)

    tonnetz = np.mean(
        librosa.feature.tonnetz(
            y=harmonic,
            sr=sr
        ).T,
        axis=0
    )

    # Zero Crossing Rate
    zcr = np.mean(
        librosa.feature.zero_crossing_rate(
            y
        ).T,
        axis=0
    )

    # RMS Energy
    rms = np.mean(
        librosa.feature.rms(
            y=y
        ).T,
        axis=0
    )

    # Spectral Centroid
    centroid = np.mean(
        librosa.feature.spectral_centroid(
            y=y,
            sr=sr
        ).T,
        axis=0
    )

    # Spectral Bandwidth
    bandwidth = np.mean(
        librosa.feature.spectral_bandwidth(
            y=y,
            sr=sr
        ).T,
        axis=0
    )

    # Spectral Rolloff
    rolloff = np.mean(
        librosa.feature.spectral_rolloff(
            y=y,
            sr=sr
        ).T,
        axis=0
    )

    features = np.hstack([
        mfcc,
        chroma,
        mel,
        contrast,
        tonnetz,
        zcr,
        rms,
        centroid,
        bandwidth,
        rolloff
    ])

    return features


# ==========================================================
# Prediction Function
# ==========================================================
def predict_parkinsons(file_path, model, scaler):

    features = extract_features(file_path)

    features = features.reshape(1, -1)

    features = scaler.transform(features)

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0]

    confidence = float(np.max(probability) * 100)

    if prediction == 0:
        result = "Healthy"
    else:
        result = "Parkinson's"

    return result, confidence
