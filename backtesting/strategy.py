
import pandas as pd

class LongOnlyStrategy:
    """
    Simple production-safe baseline:
    - 1 = long
    - 0 = no position
    """

    def generate_positions(self, df: pd.DataFrame) -> pd.Series:
        """
        Expects:
            df['prediction'] ∈ {0,1}

        Returns:
            positions aligned with next-period execution
        """
    
        positions = df["prediction"].shift(1)  # avoiding lookahead bias
        positions = positions.fillna(0)

        return positions
    