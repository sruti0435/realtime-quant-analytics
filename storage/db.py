import sqlite3
import pandas as pd

DB_PATH = "ticks.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ticks (
                timestamp INTEGER,
                symbol TEXT,
                price REAL,
                qty REAL
            )
        """)

def save_ticks(df):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("ticks", conn, if_exists="append", index=False)

def load_ticks():
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql("SELECT * FROM ticks", conn)

def load_resampled(timeframe="1min"):
    """Load and resample ticks to OHLCV format"""
    df = load_ticks()
    if df.empty:
        return df
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.set_index("timestamp")
    
    ohlcv = df.groupby("symbol").resample(timeframe).agg({
        "price": ["first", "max", "min", "last"],
        "qty": "sum"
    }).dropna()
    ohlcv.columns = ["open", "high", "low", "close", "volume"]
    return ohlcv.reset_index()