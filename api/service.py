import joblib
import pandas as pd

from db.connection import engine


FEATURE_COLUMNS = [
    "return_1",
    "ma_5",
    "ma_10",
    "volatility_10"
]


class ModelService:

    def __init__(self, model_path="models/model.pkl"):
        self.model = joblib.load(model_path)

    def load_latest_features(self, symbol: str):

        query = """
            SELECT *
            FROM stock_features
            WHERE symbol = %s
            ORDER BY timestamp DESC
            LIMIT 1;
        """

        df = pd.read_sql(
            query,
            engine,
            params=(symbol,)
        )

        if df.empty:
            raise ValueError(
                f"No feature data found for symbol: {symbol}"
            )

        return df

    def predict(self, symbol: str):

        df = self.load_latest_features(symbol)

        X = df[FEATURE_COLUMNS]

        probability = self.model.predict_proba(X)[0][1]

        prediction = int(probability > 0.5)

        timestamp = str(df["timestamp"].iloc[0])

        return {
            "symbol": symbol,
            "prediction": prediction,
            "probability": round(float(probability), 4),
            "timestamp": timestamp
        }