
def debug_check(condition, message, df=None, columns=None, stop=True):
    
    """
    Centralized debug checker.

    condition: boolean (True = error)
    message: error description
    df: optional dataframe to inspect
    columns: subset of columns to print
    stop: whether to raise error or continue
    """

    if condition:
        print("\n DEBUG ERROR:", message)

        if df is not None:
            print("\n--- Data Snapshot ---")
            if columns:
                print(df[columns].head(10))
            else:
                print(df.head(10))

        if stop:
            raise ValueError(message)
