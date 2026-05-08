
import psycopg2

conn = psycopg2.connect(
    dbname="finance",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
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

print("Table created!")