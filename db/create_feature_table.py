
from sqlalchemy import text
from db.connection import engine


def create_feature_table():
    query = """
    CREATE TABLE IF NOT EXISTS stock_features (
        id SERIAL PRIMARY KEY,
        symbol TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        close FLOAT,
        return_1 FLOAT,
        ma_5 FLOAT,
        ma_10 FLOAT,
        volatility_10 FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(symbol, timestamp)
    );
    """

    with engine.begin() as conn:
        conn.execute(text(query))


if __name__ == "__main__":
    create_feature_table()
    print("Feature table created (SQLAlchemy)")