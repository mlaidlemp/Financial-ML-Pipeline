#This converts your DB features into a ML dataset

import pandas as pd
from db.connection import engine

def load_feature_data(symbol):
    query = """
        SELECT *
        FROM stock_features
        WHERE symbol = %s
        ORDER BY timestamp ASC;
    """
    
    df = pd.read_sql(query, engine, params=(symbol,))
    return df


def create_target(df):
    df["target"] = (df["return_1"].shift(-1) > 0).astype(int)
    
    df = df.dropna()

    return df


def prepare_dataset(symbol):
    df = load_feature_data(symbol)

    if df.empty:
        raise ValueError("No feature data available")

    df = create_target(df)

    features = ["return_1", "ma_5", "ma_10", "volatility_10"]

    X = df[features]
    y = df["target"]

    return X, y, df


def train_test_split_time_series(X, y, df, test_size=0.2):
    """
    Time-series split (no shuffling).
    Keeps alignment between X, y, and original dataframe.
    """

    split_idx = int(len(X) * (1 - test_size))

    X_train = X.iloc[:split_idx]
    X_test = X.iloc[split_idx:]

    y_train = y.iloc[:split_idx]
    y_test = y.iloc[split_idx:]

    df_train = df.iloc[:split_idx]
    df_test = df.iloc[split_idx:]

    return X_train, X_test, y_train, y_test, df_train, df_test