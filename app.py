import streamlit as st
import pandas as pd
import numpy as np
import threading
from datetime import datetime
from ingestion.websocket_client import start_ws
from storage.db import load_ticks, load_resampled, save_ticks
from analytics.regression import hedge_ratio
from analytics.spread import compute_spread
from analytics.stationarity import adf_test
from analytics.correlation import rolling_correlation
from alerts.rules import zscore_alert
import plotly.express as px
import plotly.graph_objects as go
import config
import time

st.set_page_config(page_title="Quant Analytics", layout="wide")

# Start WebSocket in background
if "ws_started" not in st.session_state:
    threading.Thread(target=start_ws, args=(config.SYMBOLS,), daemon=True).start()
    st.session_state.ws_started = True

st.title("📈 Real-Time Quant Analytics Dashboard")

# Sidebar controls
st.sidebar.header("⚙️ Controls")
symbols = st.sidebar.multiselect("Select Symbols", config.SYMBOLS, default=config.SYMBOLS[:2])
timeframe = st.sidebar.selectbox("Timeframe", ["1s", "1min", "5min"], index=1)
window = st.sidebar.slider("Rolling Window", 10, 200, 60)
z_thresh = st.sidebar.slider("Z-Score Alert Threshold", 1.0, 3.0, 2.0)
auto_refresh = st.sidebar.checkbox("Auto Refresh (5s)", value=False)  # Default OFF

# OHLC Upload
st.sidebar.header("📤 Upload OHLC Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV (timestamp, symbol, price, qty)", type=["csv"])
if uploaded_file:
    upload_df = pd.read_csv(uploaded_file)
    save_ticks(upload_df)
    st.sidebar.success(f"Uploaded {len(upload_df)} rows!")

# Load data
data = load_ticks()
if data.empty or len(data) < 50:
    st.warning("⏳ Waiting for data... (collecting from WebSocket)")
    st.info(f"Current rows: {len(data)}")
    st.stop()

# Process data
data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
df = data[data["symbol"].isin(symbols)]

if len(symbols) < 2:
    st.error("Select at least 2 symbols for pair analytics")
    st.stop()

pivot = df.pivot_table(index="timestamp", columns="symbol", values="price", aggfunc="last").dropna()

if len(pivot) < window:
    st.warning(f"Need {window} data points, have {len(pivot)}")
    st.stop()

# Analytics
x, y = pivot[symbols[0]].iloc[-window:], pivot[symbols[1]].iloc[-window:]
beta = hedge_ratio(x, y)
spread, z = compute_spread(x, y, beta)
adf_pval = adf_test(spread)
corr = rolling_correlation(x, y, min(20, window))

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Hedge Ratio (β)", f"{beta:.4f}")
col2.metric("ADF p-value", f"{adf_pval:.4f}", delta="Stationary" if adf_pval < 0.05 else "Non-stationary")
col3.metric("Current Z-Score", f"{z.iloc[-1]:.2f}")
col4.metric("Correlation", f"{corr.iloc[-1]:.3f}" if not np.isnan(corr.iloc[-1]) else "N/A")

# Alert
if zscore_alert(z, z_thresh):
    st.error(f"⚠️ Z-Score Alert! |z| = {abs(z.iloc[-1]):.2f} > {z_thresh}")

# Charts
tab1, tab2, tab3, tab4 = st.tabs(["📊 Prices", "📉 Spread & Z-Score", "🔗 Correlation", "📋 Data"])

with tab1:
    fig = go.Figure()
    for sym in symbols:
        fig.add_trace(go.Scatter(x=pivot.index, y=pivot[sym], name=sym, mode="lines"))
    fig.update_layout(title="Price Series", xaxis_title="Time", yaxis_title="Price", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        fig_spread = px.line(x=spread.index, y=spread.values, title="Spread")
        fig_spread.update_layout(xaxis_title="Time", yaxis_title="Spread")
        st.plotly_chart(fig_spread, use_container_width=True)
    with col2:
        fig_z = px.line(x=z.index, y=z.values, title="Z-Score")
        fig_z.add_hline(y=z_thresh, line_dash="dash", line_color="red", annotation_text=f"+{z_thresh}")
        fig_z.add_hline(y=-z_thresh, line_dash="dash", line_color="red", annotation_text=f"-{z_thresh}")
        fig_z.add_hline(y=0, line_dash="dot", line_color="gray")
        st.plotly_chart(fig_z, use_container_width=True)

with tab3:
    fig_corr = px.line(x=corr.index, y=corr.values, title=f"Rolling Correlation (window={min(20, window)})")
    fig_corr.update_layout(xaxis_title="Time", yaxis_title="Correlation")
    st.plotly_chart(fig_corr, use_container_width=True)

with tab4:
    st.subheader("Raw Data")
    st.dataframe(pivot.tail(100), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Download Prices CSV", pivot.to_csv(), "prices.csv", "text/csv")
    with col2:
        analytics_df = pd.DataFrame({"spread": spread, "z_score": z, "correlation": corr})
        st.download_button("📥 Download Analytics CSV", analytics_df.to_csv(), "analytics.csv", "text/csv")

# Footer stats
st.sidebar.markdown("---")
st.sidebar.caption(f"📊 Total ticks: {len(data)}")
st.sidebar.caption(f"🕐 Last update: {datetime.now().strftime('%H:%M:%S')}")

# Auto-refresh at the END (after everything renders)
if auto_refresh:
    time.sleep(5)
    st.rerun()