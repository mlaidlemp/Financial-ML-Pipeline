import joblib
import pandas as pd

from datetime import datetime, UTC

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from db.connection import engine
from core.logging import get_logger


logger = get_logger(__name__)


FEATURES = [
    "return_1d",
    "return_5d",
    "ma_10",
    "ma_20",
    "volatility_10"
]


QUERY = "SELECT * FROM stock_features"



def train_model():
    df = pd.read_sql(QUERY, engine)

    X = df[FEATURES]
    y = df["target"]

    split_idx = int(len(df) * 0.8)

    X_train = X.iloc[:split_idx]
    X_test = X.iloc[split_idx:]

    y_train = y.iloc[:split_idx]
    y_test = y.iloc[split_idx:]

    model = Pipeline([
        ("scaler", StandardScaler()),
        (
            "model",
            RandomForestRegressor(
                n_estimators=200,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        )
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    logger.info(f"Model MAE: {mae}")

    artifact = {
        "model": model,
        "features": FEATURES,
        "trained_at": datetime.now(UTC).isoformat(),
        "metrics": {
            "mae": mae
        }
    }

    joblib.dump(artifact, "artifacts/model.pkl")

    logger.info("Model saved")


if __name__ == "__main__":
    train_model()