# Financial ML Pipeline

A production-oriented end-to-end financial machine learning system for stock market data ingestion, feature engineering, model training, backtesting, API serving, containerization, and cloud deployment.

This project was designed with real-world ML engineering and quantitative finance workflows in mind, focusing on modular architecture, reproducibility, and scalable infrastructure rather than notebook-based experimentation.

# Core Features
- Automated stock market data ingestion using Yahoo Finance (yfinance)
- PostgreSQL-based persistent storage
- Incremental ETL and feature engineering pipeline
- Time-series aware machine learning workflow
- Random Forest classification model for directional prediction
- Backtesting engine with:
  - Profit & Loss (PnL)
  - Sharpe Ratio
  - Maximum Drawdown
- FastAPI-based inference API
- Dockerized deployment
- CI/CD automation using GitHub Actions
- Cloud deployment architecture ready
- Modular production-style project structure
