import joblib
import pandas as pd


class ModelService:
    def __init__(self, model_path="models/model.pkl"):
        self.model = joblib.load(model_path)

    def predict(self, symbol: str):

        sample_data = pd.DataFrame([{
            "return_1": 0.01,
            "ma_5": 150,
            "ma_10": 148,
            "volatility_10": 0.02
        }])

        prob = self.model.predict_proba(sample_data)[0][1]
        pred = int(prob > 0.5)

        return {
            "symbol": symbol,
            "prediction": pred,
            "probability": float(prob)
        }