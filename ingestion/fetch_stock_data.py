import pandas as pd
import yfinance as yf
from sqlalchemy import text

from db.connection import engine
from core.logging import get_logger


logger = get_logger(__name__)


SYMBOLS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META"
]


CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    timestamp TIMESTAMP,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT
)
"""


with engine.begin() as conn:
    conn.execute(text(CREATE_TABLE_QUERY))



def fetch_symbol(symbol: str):
    logger.info(f"Fetching data for {symbol}")

    df = yf.download(
        symbol,
        period="2y",
        interval="1d",
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        logger.warning(f"No data found for {symbol}")
        return

    df.reset_index(inplace=True)

    df.columns = [
        c[0].lower() if isinstance(c, tuple) else c.lower()
        for c in df.columns
    ]

    df["symbol"] = symbol

    df["date"] = pd.to_datetime(df["date"], utc=True)

    df.rename(columns={"date": "timestamp"}, inplace=True)

    df.to_sql(
        "stock_prices",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    logger.info(f"Inserted {len(df)} rows for {symbol}")


if __name__ == "__main__":
    for symbol in SYMBOLS:
        fetch_symbol(symbol)