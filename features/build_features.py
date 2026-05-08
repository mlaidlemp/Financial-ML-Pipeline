
import pandas as pd
import logging
import psycopg2

from db.connection import engine
from features.feature_store import get_latest_feature_timestamp

# Logging setup
logging.basicConfig(
    filename="logs/features.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_new_data(symbol):
    last_ts = get_latest_feature_timestamp(symbol)

    if last_ts is None:
        query = """
            SELECT timestamp, close
            FROM stock_prices
            WHERE symbol = %s
            ORDER BY timestamp ASC;
        """
        params = (symbol,)
    else:
        query = """
            SELECT timestamp, close
            FROM stock_prices
            WHERE symbol = %s AND timestamp > %s
            ORDER BY timestamp ASC;
        """
        params = (symbol, last_ts)
    df = pd.read_sql(query, engine, params=params)
    return df


def build_features(df):
    df = df.sort_values("timestamp")
    
    df["return_1"] = df["close"].pct_change()
    df["ma_5"] = df["close"].rolling(5).mean()
    df["ma_10"] = df["close"].rolling(10).mean()
    df["volatility_10"] = df["return_1"].rolling(10).std()

    df = df.dropna()

    return df

def save_features(df, symbol):
    conn = psycopg2.connect(
        dbname="finance",
        user="admin",
        password="admin",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    data = [
        (
            symbol,
            row.timestamp,
            row.close,
            row.return_1,
            row.ma_5,
            row.ma_10,
            row.volatility_10
        )
        for row in df.itertuples()
    ]

    cursor.executemany("""
        INSERT INTO stock_features
        (symbol, timestamp, close, return_1, ma_5, ma_10, volatility_10)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, timestamp) DO NOTHING;
    """, data)

    conn.commit()
    conn.close()

    logging.info(f"Inserted {len(data)} rows")


def main():
    symbol = "AAPL"

    logging.info("Starting feature pipeline")

    df = load_new_data(symbol)

    if df.empty:
        logging.info("No new data")
        return

    df = build_features(df)

    if df.empty:
        logging.warning("Not enough data after feature generation")
        return

    save_features(df, symbol)

    logging.info("Feature pipeline completed")


if __name__ == "__main__":
    main()