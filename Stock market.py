import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta

# ── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("Stock Market Analysis Dashboard")

# ── SIDEBAR (user controls) ───────────────────────────────────
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Enter stock ticker", value="AAPL").upper()
period = st.sidebar.selectbox("Time period", ["1mo", "3mo", "6mo", "1y", "2y"])

# ── FETCH DATA ────────────────────────────────────────────────
@st.cache_data(ttl=300)   # cache for 5 mins so it doesn't re-fetch every click
def load_data(ticker, period):
    df = yf.Ticker(ticker).history(period=period)
    df.index = pd.to_datetime(df.index)
    return df

df = load_data(ticker, period)

# Stop and show error if ticker is wrong
if df.empty:
    st.error(f"No data found for '{ticker}'. Check the ticker symbol.")
    st.stop()

# ── CALCULATE INDICATORS ──────────────────────────────────────
df["MA_20"] = df["Close"].rolling(20).mean()
df["MA_50"] = df["Close"].rolling(50).mean()
df["RSI"]   = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()

bb = ta.volatility.BollingerBands(df["Close"])
df["BB_Upper"] = bb.bollinger_hband()
df["BB_Lower"] = bb.bollinger_lband()

# ── KPI METRICS ROW ───────────────────────────────────────────
latest_price  = df["Close"].iloc[-1]
prev_price    = df["Close"].iloc[-2]
price_change  = ((latest_price - prev_price) / prev_price) * 100
week_high     = df["High"].max()
week_low      = df["Low"].min()
avg_volume    = df["Volume"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Price",  f"${latest_price:.2f}",  f"{price_change:+.2f}%")
col2.metric("Period High",    f"${week_high:.2f}")
col3.metric("Period Low",     f"${week_low:.2f}")
col4.metric("Avg Daily Volume", f"{avg_volume:,.0f}")

st.divider()

# ── MAIN CANDLESTICK CHART ────────────────────────────────────
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    row_heights=[0.7, 0.3],
    vertical_spacing=0.05
)

# Candlestick
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["Open"], high=df["High"],
    low=df["Low"],   close=df["Close"],
    name=ticker
), row=1, col=1)

# Moving averages on the same chart
fig.add_trace(go.Scatter(
    x=df.index, y=df["MA_20"],
    line=dict(color="royalblue", width=1.5),
    name="MA 20"
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=df.index, y=df["MA_50"],
    line=dict(color="orange", width=1.5),
    name="MA 50"
), row=1, col=1)

# Bollinger Bands
fig.add_trace(go.Scatter(
    x=df.index, y=df["BB_Upper"],
    line=dict(color="gray", width=1, dash="dash"),
    name="BB Upper"
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=df["BB_Lower"],
    line=dict(color="gray", width=1, dash="dash"),
    name="BB Lower", fill="tonexty", fillcolor="rgba(200,200,200,0.1)"
), row=1, col=1)

# Volume bars
colors = ["green" if c >= o else "red"
          for c, o in zip(df["Close"], df["Open"])]
fig.add_trace(go.Bar(
    x=df.index, y=df["Volume"],
    marker_color=colors, name="Volume", opacity=0.6
), row=2, col=1)

fig.update_layout(
    title=f"{ticker} — Price, Volume & Indicators",
    xaxis_rangeslider_visible=False,
    height=600,
    showlegend=True
)
fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
fig.update_yaxes(title_text="Volume",      row=2, col=1)

st.plotly_chart(fig, use_container_width=True)

# ── RSI CHART ─────────────────────────────────────────────────
st.subheader("RSI — Relative Strength Index (14)")
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(
    x=df.index, y=df["RSI"],
    line=dict(color="purple", width=2), name="RSI"
))
fig_rsi.add_hline(y=70, line_color="red",   line_dash="dash",
                  annotation_text="Overbought (70)")
fig_rsi.add_hline(y=30, line_color="green", line_dash="dash",
                  annotation_text="Oversold (30)")
fig_rsi.update_layout(height=300, yaxis=dict(range=[0, 100]))
st.plotly_chart(fig_rsi, use_container_width=True)

# ── RAW DATA TABLE ────────────────────────────────────────────
with st.expander("View raw data (last 30 days)"):
    st.dataframe(
        df[["Open","High","Low","Close","Volume"]].tail(30).round(2),
        use_container_width=True
    )

# ── FOOTER ────────────────────────────────────────────────────
st.caption("Data sourced from Yahoo Finance via yfinance. Refresh page to get latest prices.")