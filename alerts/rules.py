def zscore_alert(z, threshold):
    return abs(z.iloc[-1]) > threshold
