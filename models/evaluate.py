
import joblib
import numpy as np
from models.dataset import prepare_dataset


def evaluate():
    symbol = "AAPL"

    X, y, df = prepare_dataset(symbol)

    split_index = int(len(X) * 0.8)

    X_test = X.iloc[split_index:]

    y_test = y.iloc[split_index:]

    model = joblib.load("models/model.pkl")

    probs = model.predict_proba(X_test)[:, 1]
    
    preds = (probs > 0.5).astype(int)

    accuracy = (preds == y_test).mean()

    print(f"Accuracy: {accuracy:.4f}")

    returns = df["return_1"].iloc[split_index:]
    
    strategy_returns = returns * preds

    cumulative_return = np.cumsum(strategy_returns)
    
    print(f"Total strategy return: {cumulative_return.iloc[-1]:.4f}")

if __name__ == "__main__":
    evaluate()