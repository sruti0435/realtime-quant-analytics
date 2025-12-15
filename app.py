import streamlit as st
import pandas as pd
import threading
from ingestion.websocket_client import start_ws
from storage.db import load_ticks
from analytics.regression import hedge_ratio
from analytics.spread import compute_spread
from analytics.stationarity import adf_test
from alerts.rules import zscore_alert
import plotly.express as px
import config

st.set_page_config(layout="wide")

if "ws_started" not in st.session_state:
    threading.Thread(
        target=start_ws,
        args=(config.SYMBOLS,),
        daemon=True
    ).start()
    st.session_state.ws_started = True

st.title("Real-Time Quant Analytics Dashboard")

data = load_ticks()
if len(data) < 50:
    st.warning("Waiting for data...")
    st.stop()

symbols = st.multiselect("Select pair", config.SYMBOLS, default=config.SYMBOLS[:2])
window = st.slider("Rolling window", 20, 200, 60)
z_thresh = st.slider("Z-score alert", 1.0, 3.0, 2.0)

df = data[data["symbol"].isin(symbols)]
pivot = df.pivot(index="timestamp", columns="symbol", values="price").dropna()

x, y = pivot.iloc[-window:, 0], pivot.iloc[-window:, 1]
beta = hedge_ratio(x, y)
spread, z = compute_spread(x, y, beta)

st.metric("Hedge Ratio", round(beta, 4))
st.metric("ADF p-value", round(adf_test(spread), 4))

if zscore_alert(z, z_thresh):
    st.error("⚠ Z-score alert triggered")

fig = px.line(z, title="Z-Score")
st.plotly_chart(fig, use_container_width=True)

st.download_button(
    "Download CSV",
    data=pivot.to_csv(),
    file_name="processed_data.csv"
)
