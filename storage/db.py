import sqlite3
import pandas as pd

def save_ticks(df):
    with sqlite3.connect("ticks.db") as conn:
        df.to_sql("ticks", conn, if_exists="append", index=False)

def load_ticks():
    with sqlite3.connect("ticks.db") as conn:
        return pd.read_sql("SELECT * FROM ticks", conn)
