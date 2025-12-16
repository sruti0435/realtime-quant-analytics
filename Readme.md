# 📈 Real-Time Quant Analytics Dashboard

A real-time quantitative analytics dashboard for pair-based market diagnostics using live tick data from Binance WebSocket streams. Built for traders and researchers at quantitative trading firms focused on statistical arbitrage and market-making strategies.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/sruti0435/realtime-quant-analytics.git
cd realtime-quant-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## ✨ Features

### 📡 Data Ingestion
- **Live WebSocket** connection to Binance for real-time tick data
- **Multi-symbol support** (BTCUSDT, ETHUSDT by default)
- **CSV upload** for historical/external OHLC data
- **SQLite persistence** for tick storage

### 📊 Analytics Suite

| Metric | Description | Use Case |
|--------|-------------|----------|
| **Hedge Ratio (β)** | OLS regression coefficient | Optimal hedge position sizing |
| **Spread** | Price differential (Y - β×X) | Mean-reversion signal |
| **Z-Score** | Standardized spread | Entry/exit signals |
| **ADF Test** | Augmented Dickey-Fuller p-value | Stationarity validation |
| **Rolling Correlation** | Dynamic correlation coefficient | Regime detection |

### 🖥️ Interactive Dashboard
- **Price Charts** - Multi-asset time series with zoom/pan/hover
- **Spread & Z-Score** - Mean-reversion indicators with threshold lines
- **Correlation Plot** - Rolling correlation dynamics
- **Data Table** - Raw data inspection with CSV export

### ⚠️ Alerting System
- Configurable Z-score threshold alerts
- Visual alert banners when thresholds are breached
- Real-time monitoring capability

### 🎛️ Controls
- Symbol multi-select
- Timeframe selection (1s, 1min, 5min)
- Rolling window adjustment (10-200 periods)
- Z-score threshold slider (1.0-3.0)
- Auto-refresh toggle

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REAL-TIME QUANT ANALYTICS                        │
└─────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
  │   Binance    │──────▶│  WebSocket   │──────▶│ Tick Buffer  │
  │  WebSocket   │ ticks │   Client     │       │  (Memory)    │
  └──────────────┘       └──────────────┘       └──────┬───────┘
                                                       │
  ┌──────────────┐                              ┌──────▼───────┐
  │  CSV Upload  │─────────────────────────────▶│   SQLite     │
  │  (Manual)    │                              │   Database   │
  └──────────────┘                              └──────┬───────┘
                                                       │
                         ┌─────────────────────────────▼─────────────┐
                         │           ANALYTICS ENGINE                │
                         │  • OLS Regression  • Spread/Z-Score      │
                         │  • ADF Test        • Rolling Correlation │
                         └───────────────────┬───────────────────────┘
                                             │
              ┌──────────────────────────────┼──────────────────┐
              ▼                              ▼                  ▼
  ┌──────────────────┐          ┌──────────────────┐   ┌──────────────┐
  │    STREAMLIT     │          │     ALERTS       │   │  CSV EXPORT  │
  │    DASHBOARD     │          │  (Z-Score > n)   │   │              │
  └──────────────────┘          └──────────────────┘   └──────────────┘
```

### Project Structure

```
├── app.py                    # Main Streamlit dashboard
├── config.py                 # Configuration (symbols, settings)
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
│
├── ingestion/
│   ├── websocket_client.py   # Binance WebSocket connection
│   └── tick_buffer.py        # In-memory tick buffer
│
├── storage/
│   └── db.py                 # SQLite operations & resampling
│
├── analytics/
│   ├── regression.py         # OLS hedge ratio calculation
│   ├── spread.py             # Spread & z-score computation
│   ├── stationarity.py       # ADF test implementation
│   └── correlation.py        # Rolling correlation
│
└── alerts/
    └── rules.py              # Alert logic (z-score threshold)
```

---

## 📖 Methodology

### Hedge Ratio (OLS Regression)
The hedge ratio β is computed using Ordinary Least Squares regression:
```
Y = α + β×X + ε
```
Where Y and X are price series of the two assets.

### Spread Calculation
```
Spread = Y - β×X
```

### Z-Score Normalization
```
Z = (Spread - μ) / σ
```
Where μ is the rolling mean and σ is the rolling standard deviation.

### ADF Test
The Augmented Dickey-Fuller test checks for stationarity:
- **p-value < 0.05**: Spread is stationary (mean-reverting) ✅
- **p-value > 0.05**: Spread is non-stationary ❌

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.13 |
| Frontend | Streamlit |
| Database | SQLite |
| Charts | Plotly |
| Analytics | pandas, numpy, statsmodels |
| Data Feed | Binance WebSocket API |

---

## 📤 Data Export

The dashboard provides CSV export for:
1. **Price Data** - Raw OHLC prices for selected symbols
2. **Analytics Data** - Computed spread, z-score, and correlation values

---

## 🔮 Future Extensions

- [ ] Kalman Filter for dynamic hedge estimation
- [ ] Robust regression (Huber/Theil-Sen)
- [ ] Mini mean-reversion backtest
- [ ] Cross-correlation heatmaps
- [ ] Liquidity filters
- [ ] WebSocket reconnection handling

---

## 📝 AI Usage Transparency

This project utilized Claude (Anthropic) for:
- Debugging WebSocket connection and environment issues
- Structuring the Streamlit dashboard layout
- Implementing analytics functions
- Code review and optimization
- Documentation generation

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Sruti Totawad**

- GitHub: [@sruti0435](https://github.com/sruti0435)

