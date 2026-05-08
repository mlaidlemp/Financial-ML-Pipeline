
import pandas as pd


class BacktestEngine:
    def __init__(
        self,
        initial_capital: float = 100000,
        transaction_cost: float = 0.0005  # 5 bps
    ):
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost

    def run(self, df: pd.DataFrame, positions: pd.Series) -> pd.DataFrame:
        """
        Required columns:
            df['return_1']

        positions:
            0 or 1 (no shorting yet)
        """

        df = df.copy()
        df["position"] = positions.fillna(0)

        df["strategy_return"] = df["position"] * df["return_1"]

        df["trade"] = df["position"].diff().abs().fillna(0)
        
        df["cost"] = df["trade"] * self.transaction_cost

        df["net_return"] = df["strategy_return"] - df["cost"]

        df["net_return"] = df["net_return"].fillna(0)

        df["equity"] = (1 + df["net_return"]).cumprod() * self.initial_capital

        return df