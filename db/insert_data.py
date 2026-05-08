import psycopg2

def insert_stock_data(data, symbol):
    conn = psycopg2.connect(
        dbname="finance",
        user="admin",
        password="admin",
        host="localhost",
        port="5432"
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
    conn.close()