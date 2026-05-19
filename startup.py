from db.init_db import create_price_table
from db.create_feature_table import create_feature_table

from ingestion.fetch_stock_data import fetch_stock_data
from features.build_features import build_features

from models.train_model import train


def initialize_system():

    print("Creating stock_prices table...")
    create_price_table()

    print("Creating stock_features table...")
    create_feature_table()

    print("Fetching stock data...")
    fetch_stock_data()

    print("Building features...")
    build_features()

    print("Training model...")
    train()

    print("System initialization complete")


if __name__ == "__main__":
    initialize_system()