
import numpy as np
import pandas as pd


class PerformanceMetrics:
    @staticmethod
    def sharpe_ratio(returns: pd.Series, freq: int = 252) -> float:
        mean = returns.mean()
        std = returns.std()

        if std == 0:
            return 0.0

        return (mean / std) * np.sqrt(freq)

    @staticmethod
    def max_drawdown(equity: pd.Series) -> float:
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        return drawdown.min()

    @staticmethod
    def total_return(equity: pd.Series) -> float:
        return (equity.iloc[-1] / equity.iloc[0]) - 1

    @staticmethod
    def compute_all(df: pd.DataFrame) -> dict:
        return {
            "total_return": PerformanceMetrics.total_return(df["equity"]),
            "sharpe_ratio": PerformanceMetrics.sharpe_ratio(df["net_return"]),
            "max_drawdown": PerformanceMetrics.max_drawdown(df["equity"]),
        }
    