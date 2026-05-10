import os
import psycopg2


def insert_stock_data(data, symbol):

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "finance"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "admin"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

    cursor = conn.cursor()

    for row in data:
        try:
            cursor.execute("""
                INSERT INTO stock_prices 
                (symbol, timestamp, close)
                VALUES (%s, %s, %s)
                ON CONFLICT (symbol, timestamp) DO NOTHING;
            """, (
                symbol,
                row["timestamp"],
                row["close"]
            ))

        except Exception as e:
            print("Insert error:", e)

    conn.commit()

    cursor.close()
    conn.close()