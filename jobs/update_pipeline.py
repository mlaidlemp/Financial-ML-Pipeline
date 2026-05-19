from ingestion.fetch_stock_data import fetch_stock_data
from features.build_features import build_features
from models.train_model import train


def run_pipeline():

    print("Fetching stock data...")
    fetch_stock_data()

    print("Building features...")
    build_features()

    print("Training model...")
    train()

    print("Pipeline update complete")


if __name__ == "__main__":
    run_pipeline()