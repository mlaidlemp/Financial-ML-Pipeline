import pandas as pd
from sqlalchemy import text

from db.connection import engine
from core.logging import get_logger


logger = get_logger(__name__)


FEATURE_QUERY = """
SELECT *
FROM stock_prices
ORDER BY timestamp ASC
"""


CREATE_FEATURE_TABLE = """
CREATE TABLE IF NOT EXISTS stock_features (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    timestamp TIMESTAMP,
    return_1d FLOAT,
    return_5d FLOAT,
    ma_10 FLOAT,
    ma_20 FLOAT,
    volatility_10 FLOAT,
    target FLOAT
)
"""


with engine.begin() as conn:
    conn.execute(text(CREATE_FEATURE_TABLE))



def build_features():
    df = pd.read_sql(FEATURE_QUERY, engine)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    frames = []

    for symbol in df["symbol"].unique():
        sdf = df[df["symbol"] == symbol].copy()

        sdf["return_1d"] = sdf["close"].pct_change(1)
        sdf["return_5d"] = sdf["close"].pct_change(5)

        sdf["ma_10"] = sdf["close"].rolling(10).mean()
        sdf["ma_20"] = sdf["close"].rolling(20).mean()

        sdf["volatility_10"] = (
            sdf["return_1d"]
            .rolling(10)
            .std()
        )

        sdf["target"] = sdf["close"].shift(-1)

        sdf.dropna(inplace=True)

        frames.append(sdf)

    final_df = pd.concat(frames)

    feature_cols = [
        "symbol",
        "timestamp",
        "return_1d",
        "return_5d",
        "ma_10",
        "ma_20",
        "volatility_10",
        "target"
    ]

    final_df[feature_cols].to_sql(
        "stock_features",
        engine,
        if_exists="replace",
        index=False,
        method="multi"
    )

    logger.info("Feature engineering complete")


if __name__ == "__main__":
    build_features()