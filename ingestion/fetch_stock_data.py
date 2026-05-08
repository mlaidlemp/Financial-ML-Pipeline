import yfinance as yf
import pandas as pd
import logging

from db.insert_data import insert_stock_data

logging.basicConfig(
    filename="logs/ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

STOCK_SYMBOL = "AAPL"


def fetch_stock_data(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="5d", interval="1h")

        if df.empty:
            raise ValueError("No data received")

        return df

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return None


def process_and_store_data(df: pd.DataFrame, symbol: str):
    try:
        df = df.reset_index()

        print("Columns from yfinance:", df.columns)

        if "Datetime" in df.columns:
            time_col = "Datetime"
        elif "Date" in df.columns:
            time_col = "Date"
        else:
            raise ValueError(f"No valid time column found: {df.columns}")

        df = df[[time_col, "Close"]]

        df.columns = ["timestamp", "close"]

        data = df.to_dict(orient="records")

        insert_stock_data(data, symbol)

        logging.info(f"Inserted {len(data)} rows into database for {symbol}")

    except Exception as e:
        logging.error(f"Error processing/storing data: {e}")
        print("Insert error:", e)

def main():
    logging.info("Starting data ingestion")

    df = fetch_stock_data(STOCK_SYMBOL)

    if df is not None:
        process_and_store_data(df, STOCK_SYMBOL)
    else:
        logging.warning("No data fetched, skipping insert")

    logging.info("Finished ingestion")


if __name__ == "__main__":
    main()