# Financial ML Pipeline

Production-grade financial machine learning pipeline for market data ingestion, feature engineering, model training, and live cloud inference serving.

Built with:

* FastAPI
* PostgreSQL
* Scikit-learn
* SQLAlchemy
* Render Cloud
* Yahoo Finance API

This project demonstrates real-world financial ML engineering, financial feature pipelines, MLOps fundamentals, and cloud-native ML deployment.

---

# Live Deployment

## Live API

https://web-financial-ml-pipeline-1.onrender.com

## Swagger API Documentation

https://web-financial-ml-pipeline-1.onrender.com/docs

## Health Endpoint

https://web-financial-ml-pipeline-1.onrender.com/health

---

# System Architecture

```text
Yahoo Finance API
        ↓
Data Ingestion Pipeline
        ↓
PostgreSQL Feature Store
        ↓
Feature Engineering Pipeline
        ↓
ML Training Pipeline
        ↓
Serialized Model Artifact (.pkl)
        ↓
FastAPI Inference Service
        ↓
Render Cloud Deployment
```

---

# Features

* Automated market data ingestion
* PostgreSQL-backed feature store
* Financial feature engineering
* Machine learning model training
* Serialized model persistence
* FastAPI inference API
* Cloud deployment on Render
* Swagger/OpenAPI documentation
* Production-ready modular architecture
* End-to-end ML pipeline orchestration

---

# Engineered Financial Features

Current engineered features include:

* Daily returns
* Rolling volatility
* Moving averages
* Multi-period return windows
* Trend indicators

The architecture is designed to support additional quant features such as:

* RSI
* MACD
* Bollinger Bands
* VWAP
* Momentum indicators
* Alpha factor generation

---

# Example API Usage

## Predict Stock Price

```bash
curl -X POST "https://web-financial-ml-pipeline-1.onrender.com/predict" \
-H "Content-Type: application/json" \
-d '{"symbol":"AAPL"}'
```

Example response:

```json
{
  "symbol": "AAPL",
  "prediction": 304.40922879225513,
  "model_version": "2026-05-22T18:57:10.319614+00:00"
}
```

---

# Supported Symbols

Currently supported equities include:

* AAPL
* MSFT
* AMZN
* GOOGL
* META

---

# Local Development Setup

## Clone Repository

```bash
git clone https://github.com/mlaidlemp/Financial-ML-Pipeline.git
cd Financial-ML-Pipeline
```

---

## Create Virtual Environment

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:5432/DATABASE_NAME?sslmode=require
```

---

# Run the Pipeline

## 1. Ingest Market Data

```bash
python -m ingestion.fetch_stock_data
```

## 2. Build Features

```bash
python -m features.build_features
```

## 3. Train Model

```bash
python -m models.train_model
```

## 4. Start API Server

```bash
uvicorn api.main:app
```

## 5. Open Swagger Docs

```text
http://127.0.0.1:8000/docs
```

---

# Project Structure

```text
Financial-ML-Pipeline/
│
├── api/
│   ├── main.py
│   ├── schemas.py
│   └── service.py
│
├── ingestion/
│   └── fetch_stock_data.py
│
├── features/
│   └── build_features.py
│
├── models/
│   └── train_model.py
│
├── db/
│   └── connection.py
│
├── core/
│   └── config.py
│
├── artifacts/
│   └── model.pkl
│
├── logs/
│
├── tests/
│
├── requirements.txt
├── render.yaml
└── README.md
```

---

# MLOps & Production Engineering

This project demonstrates:

* Production ML pipeline orchestration
* Financial data engineering
* Feature engineering workflows
* PostgreSQL integration
* Cloud-native ML deployment
* Model serialization/deserialization
* FastAPI inference serving
* Environment-based configuration
* Production debugging and deployment workflows
* Financial ML infrastructure design

---

# Deployment

The application is deployed on Render Cloud with:

* PostgreSQL database hosting
* FastAPI inference service
* Cloud-hosted prediction API
* Persistent ML feature store
