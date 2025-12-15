import pandas as pd

BUFFER = []

def add_tick(tick):
    BUFFER.append(tick)

def get_ticks():
    df = pd.DataFrame(BUFFER)
    BUFFER.clear()
    return df
