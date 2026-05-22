import joblib
import pandas as pd

from sqlalchemy import text

from db.connection import engine


artifact = joblib.load("artifacts/model.pkl")

model = artifact["model"]
FEATURES = artifact["features"]
MODEL_VERSION = artifact["trained_at"]


QUERY = text("""
SELECT *
FROM stock_features
WHERE symbol = :symbol
ORDER BY timestamp DESC
LIMIT 1
""")



def predict(symbol: str):
    df = pd.read_sql(
        QUERY,
        engine,
        params={"symbol": symbol}
    )

    if df.empty:
        raise ValueError("No data available")

    X = df[FEATURES]

    prediction = model.predict(X)[0]

    return {
        "symbol": symbol,
        "prediction": float(prediction),
        "model_version": MODEL_VERSION
    }