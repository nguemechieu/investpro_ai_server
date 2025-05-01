# 📈 InvestPro AI Server

A lightweight, production-ready **FastAPI + TensorFlow** server that provides real-time **BUY/SELL predictions** for financial candle data using a **Deep Neural Network (DNN)**.

Easily connect your trading bots or applications (Java, Python, etc.) via HTTP.

---

## 🚀 Features

- ✅ Deep Neural Network (DNN) powered predictions (TensorFlow 2.x)
- ✅ FastAPI server (ultra-fast HTTP)
- ✅ Real-time candle feature-based prediction
- ✅ StandardScaler normalization
- ✅ Docker & Docker Compose ready
- ✅ Lightweight deployment (< 1GB container)
- ✅ High-performance, low-latency response (< 30ms typical)

---

## 📦 Project Structure

```plaintext
investpro_ai_server.py       # Main FastAPI application
investpro_ai_dnn_model.h5     # Trained TensorFlow DNN model
investpro_scaler.pkl          # StandardScaler for feature normalization
requirements.txt              # Python dependencies
Dockerfile                    # Docker build file
docker-compose.yml            # Multi-service orchestration
README.md                     # (this file)
