import pandas as pd
def rolling_correlation(x, y, window=20):
    return x.rolling(window).corr(y)