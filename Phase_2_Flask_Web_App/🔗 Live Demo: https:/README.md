# HOPE_AI

## ParkinsonAI — Voice-Based Parkinson's Detection

An AI-powered web app that analyzes a short voice recording and predicts the likelihood of Parkinson's disease using machine learning.

🔗 **Live Demo:** https://parkinson-disese.onrender.com

### How it works
1. Say "AAAAAA..." into your microphone for 3 seconds
2. The app extracts audio features (MFCC, chroma, spectral contrast, etc.)
3. A trained ML model predicts Healthy / Parkinson's with a confidence score

### Tech stack
- Flask (backend)
- scikit-learn (ML model)
- librosa (audio feature extraction)
- Deployed on Render
