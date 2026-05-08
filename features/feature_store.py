
import pandas as pd
from db.connection import engine

def get_latest_feature_timestamp(symbol):
    query = """
        SELECT MAX(timestamp) AS max_ts
        FROM stock_features
        WHERE symbol = %s;
    """

    df = pd.read_sql(query, engine, params=(symbol,))
    
    return df["max_ts"].iloc[0]
