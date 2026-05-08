import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

from models.dataset import prepare_dataset

logging.basicConfig(
    filename="logs/model.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def train():
    symbol = "AAPL"

    logging.info("Loading dataset")

    X, y, df = prepare_dataset(symbol)

    split_index = int(len(X) * 0.8)

    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )

    logging.info("Training model")

    model.fit(X_train, y_train)

    joblib.dump(model, "models/model.pkl")
    

    logging.info("Model saved")

    return model, X_test, y_test


if __name__ == "__main__":
    train()