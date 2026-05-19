import psycopg2
import os


def create_price_table():

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_prices (
        id SERIAL PRIMARY KEY,
        symbol TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume FLOAT,
        UNIQUE(symbol, timestamp)
    );
    """)

    conn.commit()
    conn.close()

    print("stock_prices table created")


if __name__ == "__main__":
    create_price_table()