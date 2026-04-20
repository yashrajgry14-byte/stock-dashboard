import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta
import numpy as np
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Stock Detail", layout="wide")

# ── ALL STOCKS MAP ────────────────────────────────────────────
all_stocks = {
    "Reliance Industries":  "RELIANCE.NS",
    "TCS":                  "TCS.NS",
    "HDFC Bank":            "HDFCBANK.NS",
    "Infosys":              "INFY.NS",
    "ICICI Bank":           "ICICIBANK.NS",
    "Hindustan Unilever":   "HINDUNILVR.NS",
    "ITC":                  "ITC.NS",
    "Kotak Mahindra Bank":  "KOTAKBANK.NS",
    "Larsen & Toubro":      "LT.NS",
    "Axis Bank":            "AXISBANK.NS",
    "State Bank of India":  "SBIN.NS",
    "Bajaj Finance":        "BAJFINANCE.NS",
    "Bharti Airtel":        "BHARTIARTL.NS",
    "Asian Paints":         "ASIANPAINT.NS",
    "Maruti Suzuki":        "MARUTI.NS",
    "HCL Technologies":     "HCLTECH.NS",
    "Sun Pharma":           "SUNPHARMA.NS",
    "Titan Company":        "TITAN.NS",
    "Wipro":                "WIPRO.NS",
    "Ultratech Cement":     "ULTRACEMCO.NS",
    "Nestle India":         "NESTLEIND.NS",
    "Power Grid":           "POWERGRID.NS",
    "NTPC":                 "NTPC.NS",
    "Tech Mahindra":        "TECHM.NS",
    "Bajaj Finserv":        "BAJAJFINSV.NS",
    "Adani Ports":          "ADANIPORTS.NS",
    "Adani Enterprises":    "ADANIENT.NS",
    "Tata Motors":          "TATAMOTORS.NS",
    "JSW Steel":            "JSWSTEEL.NS",
    "Tata Steel":           "TATASTEEL.NS",
    "Dr Reddy's":           "DRREDDY.NS",
    "Cipla":                "CIPLA.NS",
    "Divis Laboratories":   "DIVISLAB.NS",
    "Eicher Motors":        "EICHERMOT.NS",
    "Hero MotoCorp":        "HEROMOTOCO.NS",
    "Bajaj Auto":           "BAJAJ-AUTO.NS",
    "Grasim Industries":    "GRASIM.NS",
    "IndusInd Bank":        "INDUSINDBK.NS",
    "Hindalco":             "HINDALCO.NS",
    "Coal India":           "COALINDIA.NS",
    "ONGC":                 "ONGC.NS",
    "IOC":                  "IOC.NS",
    "BPCL":                 "BPCL.NS",
    "Tata Consumer":        "TATACONSUM.NS",
    "Havells India":        "HAVELLS.NS",
    "Pidilite Industries":  "PIDILITIND.NS",
    "Dmart":                "DMART.NS",
    "Zomato":               "ZOMATO.NS",
    "Vedanta":              "VEDL.NS",
    "Tata Power":           "TATAPOWER.NS",
    "Siemens India":        "SIEMENS.NS",
    "Godrej Consumer":      "GODREJCP.NS",
    "Marico":               "MARICO.NS",
    "Dabur India":          "DABUR.NS",
    "Colgate Palmolive":    "COLPAL.NS",
    "Berger Paints":        "BERGEPAINT.NS",
    "Ambuja Cements":       "AMBUJACEM.NS",
    "Shree Cement":         "SHREECEM.NS",
    "Muthoot Finance":      "MUTHOOTFIN.NS",
    "SBI Life Insurance":   "SBILIFE.NS",
    "HDFC Life":            "HDFCLIFE.NS",
    "LIC India":            "LICI.NS",
    "PFC":                  "PFC.NS",
    "REC Limited":          "RECLTD.NS",
    "IRFC":                 "IRFC.NS",
    "Mankind Pharma":       "MANKIND.NS",
    "Torrent Pharma":       "TORNTPHARM.NS",
    "Lupin":                "LUPIN.NS",
    "Aurobindo Pharma":     "AUROPHARMA.NS",
    "Biocon":               "BIOCON.NS",
    "Bosch":                "BOSCHLTD.NS",
    "Ashok Leyland":        "ASHOKLEY.NS",
    "TVS Motor":            "TVSMOTOR.NS",
    "MRF":                  "MRF.NS",
    "Bharat Electronics":   "BEL.NS",
    "HAL":                  "HAL.NS",
    "IRCTC":                "IRCTC.NS",
    "Indigo":               "INDIGO.NS",
    "Jubilant Foodworks":   "JUBLFOOD.NS",
    "Trent":                "TRENT.NS",
    "Varun Beverages":      "VBL.NS",
    "Bank of Baroda":       "BANKBARODA.NS",
    "Punjab National Bank": "PNB.NS",
    "Federal Bank":         "FEDERALBNK.NS",
    "AU Small Finance":     "AUBANK.NS",
    "LTIMindtree":          "LTIM.NS",
    "Mphasis":              "MPHASIS.NS",
    "Persistent":           "PERSISTENT.NS",
    "Coforge":              "COFORGE.NS",
    "Alkem Labs":           "ALKEM.NS",
    "Britannia":            "BRITANNIA.NS",
    "SAIL":                 "SAIL.NS",
    "NMDC":                 "NMDC.NS",
    "Jindal Steel":         "JINDALSTEL.NS",
    "APL Apollo":           "APLAPOLLO.NS",
    "Motherson":            "MOTHERSON.NS",
    "DLF":                  "DLF.NS",
    "Godrej Properties":    "GODREJPROP.NS",
    "Oberoi Realty":        "OBEROIRLTY.NS",
    "Prestige Estates":     "PRESTIGE.NS",
    "Phoenix Mills":        "PHOENIXLTD.NS",
    "Macrotech":            "LODHA.NS",
    "Sobha":                "SOBHA.NS",
    "Brigade":              "BRIGADE.NS",
    "Adani Green":          "ADANIGREEN.NS",
    "Adani Power":          "ADANIPOWER.NS",
    "GAIL":                 "GAIL.NS",
    "GMR Airports":         "GMRINFRA.NS",
    "Tata Communications":  "TATACOMM.NS",
}

ticker_to_name = {v: k for k, v in all_stocks.items()}

# ── HELPERS ───────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data(tkr, period):
    df = yf.Ticker(tkr).history(period=period)
    df.index = pd.to_datetime(df.index)
    return df

@st.cache_data(ttl=3600)
def load_full(tkr):
    df = yf.Ticker(tkr).history(period="max")
    df.index = pd.to_datetime(df.index)
    return df

@st.cache_data(ttl=600)
def get_info(tkr):
    try:
        return yf.Ticker(tkr).info
    except:
        return {}

@st.cache_data(ttl=600)
def get_news(company, sector):
    articles = []
    for q in [f"{company} stock NSE", f"{company} results deal",
               f"{sector} India" if sector else company]:
        try:
            url  = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=en-IN&gl=IN&ceid=IN:en"
            resp = requests.get(url, timeout=5)
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item")[:4]:
                t = item.findtext("title", "")
                if t:
                    articles.append({
                        "title":   t,
                        "link":    item.findtext("link",    "#"),
                        "source":  item.findtext("source",  ""),
                        "pubdate": item.findtext("pubDate", "")[:16],
                    })
        except:
            continue
    seen, out = set(), []
    for a in articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            out.append(a)
    return out[:12]

def cat_news(title):
    t = title.lower()
    if any(k in t for k in ["deal","order","contract","wins","bags","merger","acqui"]):
        return "Deal / Order", "green"
    if any(k in t for k in ["result","profit","revenue","earnings","quarterly","loss"]):
        return "Earnings", "blue"
    if any(k in t for k in ["policy","rbi","sebi","regulation","budget","tax"]):
        return "Policy", "orange"
    if any(k in t for k in ["ceo","board","appoint","resign","promoter","dividend","buyback"]):
        return "Corporate", "violet"
    return "General", "gray"

def normalise(arr):
    mn, mx = arr.min(), arr.max()
    return (arr - mn) / (mx - mn) if mx != mn else arr * 0

# ── READ QUERY PARAMS ─────────────────────────────────────────
ticker       = st.query_params.get("ticker", "RELIANCE.NS")
back_index   = st.query_params.get("from",   "")
stock_name   = ticker_to_name.get(ticker, ticker.replace(".NS", ""))

# ── BACK BUTTON ───────────────────────────────────────────────
if back_index:
    encoded = requests.utils.quote(back_index)
    st.markdown(f"[← Back to {back_index}](/index_detail?index={encoded})")
else:
    st.markdown("[← Back to dashboard](/)")

st.title(stock_name)

# ── FETCH DATA ────────────────────────────────────────────────
info       = get_info(ticker)
sector     = info.get("sector",      "")
industry   = info.get("industry",    "")
mkt_cap    = info.get("marketCap",   0)
pe_ratio   = info.get("trailingPE",  None)
pb_ratio   = info.get("priceToBook", None)
div_yield  = info.get("dividendYield", None)
week52_h   = info.get("fiftyTwoWeekHigh", None)
week52_l   = info.get("fiftyTwoWeekLow",  None)
about      = info.get("longBusinessSummary", "")

if sector:
    st.caption(f"{sector} — {industry}")

# ── FUNDAMENTALS ROW ──────────────────────────────────────────
f1, f2, f3, f4, f5, f6 = st.columns(6)
f1.metric("Market Cap",
          f"₹{mkt_cap/1e9:.0f}B" if mkt_cap else "N/A")
f2.metric("P/E Ratio",
          f"{pe_ratio:.1f}" if pe_ratio else "N/A")
f3.metric("P/B Ratio",
          f"{pb_ratio:.1f}" if pb_ratio else "N/A")
f4.metric("Dividend Yield",
          f"{div_yield*100:.2f}%" if div_yield else "N/A")
f5.metric("52-week High",
          f"₹{week52_h:,.2f}" if week52_h else "N/A")
f6.metric("52-week Low",
          f"₹{week52_l:,.2f}" if week52_l else "N/A")

if about:
    with st.expander("About this company"):
        st.write(about[:800] + "..." if len(about) > 800 else about)

st.divider()

# ── PERIOD CHART ──────────────────────────────────────────────
period_map = {
    "1M": "1mo", "3M": "3mo", "6M": "6mo",
    "1Y": "1y",  "3Y": "3y",  "5Y": "5y"
}
sel = st.radio("Period", list(period_map.keys()), horizontal=True, index=3)
df  = load_data(ticker, period_map[sel])

if df.empty:
    st.error("No data found for this ticker.")
    st.stop()

p_change = ((df["Close"].iloc[-1] - df["Close"].iloc[0]) /
             df["Close"].iloc[0]) * 100
latest   = df["Close"].iloc[-1]
prev     = df["Close"].iloc[-2]
day_chg  = ((latest - prev) / prev) * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Price", f"₹{latest:,.2f}", f"{day_chg:+.2f}%")
c2.metric("Period Return", f"{p_change:+.2f}%")
c3.metric("Period High",   f"₹{df['High'].max():,.2f}")
c4.metric("Period Low",    f"₹{df['Low'].min():,.2f}")

# Candlestick + volume
df["MA_20"] = df["Close"].rolling(20).mean()
df["MA_50"] = df["Close"].rolling(50).mean()

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    row_heights=[0.7, 0.3], vertical_spacing=0.04)
fig.add_trace(go.Candlestick(
    x=df.index, open=df["Open"], high=df["High"],
    low=df["Low"], close=df["Close"], name=stock_name
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=df["MA_20"],
    line=dict(color="orange", width=1.5), name="MA 20"
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=df["MA_50"],
    line=dict(color="royalblue", width=1.5), name="MA 50"
), row=1, col=1)
colors = ["green" if c >= o else "red"
          for c, o in zip(df["Close"], df["Open"])]
fig.add_trace(go.Bar(
    x=df.index, y=df["Volume"],
    marker_color=colors, opacity=0.6, name="Volume"
), row=2, col=1)
fig.update_layout(
    height=520, xaxis_rangeslider_visible=False,
    title=f"{stock_name} — {sel} price & volume"
)
fig.update_yaxes(title_text="Price (₹)", row=1, col=1)
fig.update_yaxes(title_text="Volume",    row=2, col=1)
st.plotly_chart(fig, use_container_width=True)

# ── RSI ───────────────────────────────────────────────────────
df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
fig_rsi   = go.Figure()
fig_rsi.add_trace(go.Scatter(
    x=df.index, y=df["RSI"],
    line=dict(color="purple", width=2), name="RSI"
))
fig_rsi.add_hline(y=70, line_color="red",   line_dash="dash",
                  annotation_text="Overbought")
fig_rsi.add_hline(y=30, line_color="green", line_dash="dash",
                  annotation_text="Oversold")
fig_rsi.update_layout(height=260, yaxis=dict(range=[0, 100]),
                       title="RSI (14)")
st.plotly_chart(fig_rsi, use_container_width=True)

st.divider()

# ── PATTERN SIGNAL ────────────────────────────────────────────
st.subheader("Signal analysis")
history_df = load_full(ticker)

if len(history_df) >= 100:
    current_window = 20
    recent_prices  = history_df["Close"].iloc[-current_window:].values
    current_norm   = normalise(recent_prices)
    closes         = history_df["Close"].values
    dates          = history_df.index
    sims           = []
    search_end     = len(closes) - current_window - 60

    for i in range(current_window, search_end):
        hw   = closes[i - current_window: i]
        dist = np.sqrt(np.mean((current_norm - normalise(hw)) ** 2))
        sims.append((i, dist))

    sims.sort(key=lambda x: x[1])
    top = sims[:10]

    fwd30, fwd90 = [], []
    for idx, _ in top:
        if idx + 30 < len(closes):
            fwd30.append(((closes[idx+30]-closes[idx])/closes[idx])*100)
        if idx + 90 < len(closes):
            fwd90.append(((closes[idx+90]-closes[idx])/closes[idx])*100)

    avg30 = np.mean(fwd30) if fwd30 else 0
    avg90 = np.mean(fwd90) if fwd90 else 0
    wr30  = (sum(1 for r in fwd30 if r > 0)/len(fwd30)*100) if fwd30 else 0

    recent = history_df.tail(252).copy()
    recent["MA_50"]       = recent["Close"].rolling(50).mean()
    recent["MA_200"]      = recent["Close"].rolling(200).mean()
    recent["RSI"]         = ta.momentum.RSIIndicator(recent["Close"], 14).rsi()
    macd                  = ta.trend.MACD(recent["Close"])
    recent["MACD"]        = macd.macd()
    recent["MACD_Signal"] = macd.macd_signal()

    price    = recent["Close"].iloc[-1]
    ma50     = recent["MA_50"].iloc[-1]
    ma200    = recent["MA_200"].iloc[-1]
    rsi_val  = recent["RSI"].iloc[-1]
    macd_val = recent["MACD"].iloc[-1]
    macd_sig = recent["MACD_Signal"].iloc[-1]
    momentum = ((history_df["Close"].iloc[-1] -
                 history_df["Close"].iloc[-current_window]) /
                 history_df["Close"].iloc[-current_window]) * 100

    signals = []
    score   = 0

    if wr30 >= 65:
        signals.append(("Pattern win rate",
            f"Similar patterns gained {wr30:.0f}% of the time over 30 days",
            "Bullish", "+"))
        score += 2
    elif wr30 <= 35:
        signals.append(("Pattern win rate",
            f"Similar patterns gained only {wr30:.0f}% of the time over 30 days",
            "Bearish", "-"))
        score -= 2
    else:
        signals.append(("Pattern win rate",
            f"Mixed — {wr30:.0f}% positive over 30 days",
            "Neutral", "~"))

    if avg30 > 3:
        signals.append(("30d pattern return",
            f"Avg +{avg30:.1f}% after similar pattern",
            "Bullish", "+"))
        score += 1
    elif avg30 < -3:
        signals.append(("30d pattern return",
            f"Avg {avg30:.1f}% after similar pattern",
            "Bearish", "-"))
        score -= 1

    if price > ma50:
        signals.append(("Price vs MA50",
            "Above 50-day MA — short-term bullish",
            "Bullish", "+"))
        score += 1
    else:
        signals.append(("Price vs MA50",
            "Below 50-day MA — short-term bearish",
            "Bearish", "-"))
        score -= 1

    if ma50 > ma200:
        signals.append(("Golden/Death cross",
            "Golden cross — 50MA above 200MA",
            "Bullish", "+"))
        score += 1
    else:
        signals.append(("Golden/Death cross",
            "Death cross — 50MA below 200MA",
            "Bearish", "-"))
        score -= 1

    if rsi_val < 35:
        signals.append(("RSI",
            f"RSI {rsi_val:.1f} — oversold, potential reversal",
            "Bullish", "+"))
        score += 1
    elif rsi_val > 65:
        signals.append(("RSI",
            f"RSI {rsi_val:.1f} — overbought, potential pullback",
            "Bearish", "-"))
        score -= 1
    else:
        signals.append(("RSI",
            f"RSI {rsi_val:.1f} — neutral",
            "Neutral", "~"))

    if macd_val > macd_sig:
        signals.append(("MACD",
            "MACD above signal — positive momentum",
            "Bullish", "+"))
        score += 1
    else:
        signals.append(("MACD",
            "MACD below signal — negative momentum",
            "Bearish", "-"))
        score -= 1

    if momentum > 5:
        signals.append(("20d momentum",
            f"+{momentum:.1f}% in 20 days — strong trend",
            "Bullish", "+"))
        score += 1
    elif momentum < -5:
        signals.append(("20d momentum",
            f"{momentum:.1f}% in 20 days — selling pressure",
            "Bearish", "-"))
        score -= 1
    else:
        signals.append(("20d momentum",
            f"{momentum:.1f}% — sideways",
            "Neutral", "~"))

    if score >= 4:
        verdict, vc = "Strongly Bullish", "green"
    elif score >= 2:
        verdict, vc = "Bullish", "green"
    elif score <= -4:
        verdict, vc = "Strongly Bearish", "red"
    elif score <= -2:
        verdict, vc = "Bearish", "red"
    else:
        verdict, vc = "Neutral / Mixed", "orange"

    sig_col, news_col = st.columns([1, 1], gap="large")

    with sig_col:
        m1, m2, m3 = st.columns(3)
        m1.metric("Win rate 30d", f"{wr30:.0f}%")
        m2.metric("Avg return 30d", f"{avg30:+.1f}%")
        m3.metric("Avg return 90d", f"{avg90:+.1f}%")
        st.markdown(f"### :{vc}[{verdict}]")

        # Pattern chart
        fig_pat = go.Figure()
        fig_pat.add_trace(go.Scatter(
            y=current_norm, line=dict(color="white", width=2),
            name="Current pattern"
        ))
        for rank, (idx, _) in enumerate(top[:5]):
            hw = closes[idx - current_window: idx]
            fig_pat.add_trace(go.Scatter(
                y=normalise(hw), line=dict(width=1, dash="dot"),
                name=f"Match {rank+1}: {dates[idx].strftime('%b %Y')}"
            ))
        fig_pat.update_layout(
            title="Current vs similar historical patterns",
            height=280, yaxis_title="Normalised"
        )
        st.plotly_chart(fig_pat, use_container_width=True)

        for factor, expl, direction, sign in signals:
            color = "green" if direction=="Bullish" else \
                    "red"   if direction=="Bearish" else "orange"
            st.markdown(f"**:{color}[{sign} {factor}]**")
            st.caption(expl)

    with news_col:
        st.markdown("#### News")
        news = get_news(stock_name, sector)
        if news:
            for item in news:
                cat, color = cat_news(item["title"])
                st.markdown(
                    f":{color}[**{cat}**]  \n"
                    f"[{item['title']}]({item['link']})  \n"
                    f"<span style='font-size:11px;color:gray'>"
                    f"{item['source']} · {item['pubdate']}</span>",
                    unsafe_allow_html=True
                )
                st.markdown("---")
        else:
            st.info("No recent news found.")

            # ── BACKTESTING ENGINE ────────────────────────────────────────
st.divider()
st.subheader("Strategy backtesting engine")
st.caption("Test a trading strategy on this stock's full price history.")

bt_col1, bt_col2, bt_col3 = st.columns(3)
with bt_col1:
    strategy = st.selectbox("Select strategy", [
        "MA Crossover (20/50)",
        "MA Crossover (50/200)",
        "RSI Strategy (30/70)",
        "MACD Crossover",
        "Bollinger Band Bounce",
    ])
with bt_col2:
    initial_capital = st.number_input(
        "Initial capital (₹)", min_value=10000,
        max_value=10000000, value=100000, step=10000
    )
with bt_col3:
    bt_period = st.selectbox("Backtest period", [
        "1 Year", "3 Years", "5 Years", "10 Years", "Max"
    ], index=2)

period_lookup = {
    "1 Year": "1y", "3 Years": "3y", "5 Years": "5y",
    "10 Years": "10y", "Max": "max"
}

bt_df = load_data(ticker, period_lookup[bt_period])

if bt_df.empty or len(bt_df) < 60:
    st.warning("Not enough data for this period.")
else:
    bt_df = bt_df.copy()
    bt_df["Signal"] = 0

    if strategy == "MA Crossover (20/50)":
        bt_df["MA_fast"] = bt_df["Close"].rolling(20).mean()
        bt_df["MA_slow"] = bt_df["Close"].rolling(50).mean()
        bt_df["Signal"]  = np.where(bt_df["MA_fast"] > bt_df["MA_slow"], 1, -1)
        strategy_desc = "Buys when 20-day MA crosses above 50-day MA. Sells when it crosses below."

    elif strategy == "MA Crossover (50/200)":
        bt_df["MA_fast"] = bt_df["Close"].rolling(50).mean()
        bt_df["MA_slow"] = bt_df["Close"].rolling(200).mean()
        bt_df["Signal"]  = np.where(bt_df["MA_fast"] > bt_df["MA_slow"], 1, -1)
        strategy_desc = "Classic golden cross / death cross. Slower but filters noise."

    elif strategy == "RSI Strategy (30/70)":
        bt_df["RSI"]    = ta.momentum.RSIIndicator(bt_df["Close"], window=14).rsi()
        bt_df["Signal"] = 0
        bt_df.loc[bt_df["RSI"] < 30, "Signal"] =  1
        bt_df.loc[bt_df["RSI"] > 70, "Signal"] = -1
        strategy_desc = "Buys when RSI < 30 (oversold). Sells when RSI > 70 (overbought)."

    elif strategy == "MACD Crossover":
        macd_bt         = ta.trend.MACD(bt_df["Close"])
        bt_df["MACD"]   = macd_bt.macd()
        bt_df["MACD_S"] = macd_bt.macd_signal()
        bt_df["Signal"] = np.where(bt_df["MACD"] > bt_df["MACD_S"], 1, -1)
        strategy_desc = "Buys when MACD crosses above signal line. Sells when it crosses below."

    elif strategy == "Bollinger Band Bounce":
        bb_bt             = ta.volatility.BollingerBands(bt_df["Close"])
        bt_df["BB_upper"] = bb_bt.bollinger_hband()
        bt_df["BB_lower"] = bb_bt.bollinger_lband()
        bt_df["Signal"]   = 0
        bt_df.loc[bt_df["Close"] < bt_df["BB_lower"], "Signal"] =  1
        bt_df.loc[bt_df["Close"] > bt_df["BB_upper"], "Signal"] = -1
        strategy_desc = "Buys at lower Bollinger Band. Sells at upper Bollinger Band."

    st.markdown(f"**How this strategy works:** {strategy_desc}")
    st.divider()

    bt_df      = bt_df.dropna()
    capital    = float(initial_capital)
    shares     = 0.0
    in_trade   = False
    buy_price  = 0.0
    trades     = []
    portfolio  = []
    prev_sig   = 0

    for i, row in bt_df.iterrows():
        sig       = row["Signal"]
        price_now = row["Close"]

        if sig == 1 and prev_sig != 1 and not in_trade:
            shares    = capital / price_now
            capital   = 0.0
            buy_price = price_now
            in_trade  = True
            trades.append({
                "Date": i, "Type": "BUY",
                "Price": round(price_now, 2),
                "Shares": round(shares, 4)
            })

        elif sig == -1 and prev_sig != -1 and in_trade:
            capital  = shares * price_now
            profit   = capital - (shares * buy_price)
            in_trade = False
            trades.append({
                "Date": i, "Type": "SELL",
                "Price": round(price_now, 2),
                "Shares": round(shares, 4),
                "Profit": round(profit, 2),
                "Return%": round((price_now - buy_price) / buy_price * 100, 2)
            })
            shares = 0.0

        prev_sig = sig
        portfolio.append({"Date": i, "Value": capital + shares * price_now})

    if in_trade:
        final_price = bt_df["Close"].iloc[-1]
        capital     = shares * final_price
        trades.append({
            "Date": bt_df.index[-1], "Type": "SELL (end)",
            "Price": round(final_price, 2),
            "Shares": round(shares, 4),
            "Profit": round(capital - shares * buy_price, 2),
            "Return%": round((final_price - buy_price) / buy_price * 100, 2)
        })

    port_df      = pd.DataFrame(portfolio).set_index("Date")
    final_value  = port_df["Value"].iloc[-1]
    total_return = ((final_value - initial_capital) / initial_capital) * 100

    bh_shares = initial_capital / bt_df["Close"].iloc[0]
    bh_final  = bh_shares * bt_df["Close"].iloc[-1]
    bh_return = ((bh_final - initial_capital) / initial_capital) * 100

    nifty_bt    = load_data("^NSEI", period_lookup[bt_period])
    nifty_final = 0
    nifty_return = 0
    if not nifty_bt.empty:
        nifty_shares = initial_capital / nifty_bt["Close"].iloc[0]
        nifty_final  = nifty_shares * nifty_bt["Close"].iloc[-1]
        nifty_return = ((nifty_final - initial_capital) / initial_capital) * 100

    sell_trades  = [t for t in trades if "Return%" in t]
    winning      = [t for t in sell_trades if t["Return%"] > 0]
    win_rate_bt  = (len(winning) / len(sell_trades) * 100) if sell_trades else 0

    rolling_max  = port_df["Value"].cummax()
    drawdown     = (port_df["Value"] - rolling_max) / rolling_max * 100
    max_drawdown = drawdown.min()

    port_df["Daily_Return"] = port_df["Value"].pct_change()
    sharpe = (
        port_df["Daily_Return"].mean() /
        port_df["Daily_Return"].std() * np.sqrt(252)
    ) if port_df["Daily_Return"].std() > 0 else 0

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Final value",       f"₹{final_value:,.0f}", f"{total_return:+.1f}%")
    k2.metric("Buy & hold",        f"₹{bh_final:,.0f}",   f"{bh_return:+.1f}%")
    k3.metric("Nifty 50",          f"₹{nifty_final:,.0f}" if nifty_final else "N/A",
                                   f"{nifty_return:+.1f}%")
    k4.metric("Total trades",      len(sell_trades))
    k5.metric("Win rate",          f"{win_rate_bt:.0f}%")
    k6.metric("Max drawdown",      f"{max_drawdown:.1f}%")

    m1, m2 = st.columns(2)
    m1.metric("Sharpe ratio",      f"{sharpe:.2f}", "Good > 1.0 | Great > 2.0")
    m2.metric("Strategy vs hold",  f"{total_return - bh_return:+.1f}%",
              "Positive = strategy beat holding")

    # Portfolio chart
    fig_bt = go.Figure()
    fig_bt.add_trace(go.Scatter(
        x=port_df.index, y=port_df["Value"],
        line=dict(color="royalblue", width=2),
        name=f"{strategy}"
    ))
    bh_values = bh_shares * bt_df["Close"]
    fig_bt.add_trace(go.Scatter(
        x=bt_df.index, y=bh_values,
        line=dict(color="orange", width=1.5, dash="dash"),
        name="Buy & hold"
    ))
    if not nifty_bt.empty:
        fig_bt.add_trace(go.Scatter(
            x=nifty_bt.index, y=nifty_shares * nifty_bt["Close"],
            line=dict(color="gray", width=1.5, dash="dot"),
            name="Nifty 50"
        ))

    buy_dates  = [t["Date"] for t in trades if t["Type"] == "BUY"]
    buy_vals   = [port_df.loc[d, "Value"] if d in port_df.index
                  else initial_capital for d in buy_dates]
    sell_dates = [t["Date"] for t in trades if "SELL" in t["Type"]]
    sell_vals  = [port_df.loc[d, "Value"] if d in port_df.index
                  else final_value for d in sell_dates]

    fig_bt.add_trace(go.Scatter(
        x=buy_dates, y=buy_vals, mode="markers",
        marker=dict(color="green", size=10, symbol="triangle-up"),
        name="Buy"
    ))
    fig_bt.add_trace(go.Scatter(
        x=sell_dates, y=sell_vals, mode="markers",
        marker=dict(color="red", size=10, symbol="triangle-down"),
        name="Sell"
    ))
    fig_bt.update_layout(
        title=f"{strategy} — portfolio value vs benchmarks",
        height=500, yaxis_title="Portfolio value (₹)", hovermode="x unified"
    )
    st.plotly_chart(fig_bt, use_container_width=True)

    # Drawdown chart
    fig_dd = go.Figure()
    fig_dd.add_trace(go.Scatter(
        x=drawdown.index, y=drawdown.values,
        fill="tozeroy", fillcolor="rgba(220,0,0,0.15)",
        line=dict(color="red", width=1), name="Drawdown %"
    ))
    fig_dd.update_layout(
        title="Drawdown — how far below peak at each point",
        height=250, yaxis_title="Drawdown %"
    )
    st.plotly_chart(fig_dd, use_container_width=True)

    with st.expander(f"Full trade log ({len(sell_trades)} trades)"):
        if sell_trades:
            tdf = pd.DataFrame(sell_trades)
            tdf["Date"] = pd.to_datetime(tdf["Date"]).dt.strftime("%d %b %Y")
            st.dataframe(tdf, use_container_width=True)
            avg_ret   = np.mean([t["Return%"] for t in sell_trades])
            best_t    = max(sell_trades, key=lambda t: t["Return%"])
            worst_t   = min(sell_trades, key=lambda t: t["Return%"])
            tc1, tc2, tc3 = st.columns(3)
            tc1.metric("Avg return per trade", f"{avg_ret:+.2f}%")
            tc2.metric("Best trade",  f"+{best_t['Return%']:.1f}%")
            tc3.metric("Worst trade", f"{worst_t['Return%']:.1f}%")
        else:
            st.info("No completed trades in this period.")

    st.info(
        "Backtesting shows historical performance only. Does not account for "
        "brokerage, taxes, or slippage. NOT financial advice."
    )

st.caption("Data from Yahoo Finance. Not financial advice.")
