
import joblib

from models.dataset import prepare_dataset, train_test_split_time_series
from backtesting.strategy import LongOnlyStrategy
from backtesting.engine import BacktestEngine
from backtesting.metrics import PerformanceMetrics
from backtesting.debug import debug_check


def run_backtest(symbol="AAPL"):
    X, y, df = prepare_dataset(symbol)

    debug_check(df.empty, "Dataset is empty")

    X_train, X_test, y_train, y_test, df_train, df_test = train_test_split_time_series(
        X, y, df, test_size=0.2
    )

    debug_check(len(X_test) == 0, "Test set is empty")

    model = joblib.load("models/model.pkl")

    # Predictions
    df_test = df_test.copy()
    df_test["prob"] = model.predict_proba(X_test)[:, 1]
    
    df_test["prediction"] = (df_test["prob"] > 0.5).astype(int)
    
    debug_check(
        df_test["prediction"].isna().any(),
        "NaN values in predictions",
        df_test,
        ["prediction"]
    )


    # Strategy
    strategy = LongOnlyStrategy()
    positions = strategy.generate_positions(df_test)

    debug_check(
        positions.isna().any(),
        "NaN values in positions after shift",
        df_test,
        ["prediction"]
    )


    # Backtest engine
    engine = BacktestEngine(
        initial_capital=100000,
        transaction_cost=0.0005
    )

    results = engine.run(df_test, positions)


    debug_check(
        results["net_return"].isna().any(),
        "NaN detected in net_return",
        results,
        ["return_1", "position", "net_return"]
    )

    debug_check(
        results["equity"].isna().any(),
        "NaN detected in equity curve",
        results,
        ["equity"]
    )

    debug_check(
        len(results) == 0,
        "Backtest produced empty results"
    )


    # Metrics
    metrics = PerformanceMetrics.compute_all(results)

    print("\n=== BACKTEST RESULTS ===")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")


    print("\n=== MODEL & STRATEGY BEHAVIOR (SIGNAL ANALYSIS) ===")
    print("Position distribution:")
    print(results["position"].value_counts())

    print("\nPrediction distribution:")
    print(df_test["prediction"].value_counts())

    print("\nTrade count:", results["trade"].sum())

    print("\nAverage position size:", results["position"].mean())



    results.to_csv("data/backtest_results.csv", index=False)

    return results


if __name__ == "__main__":
    run_backtest("AAPL")