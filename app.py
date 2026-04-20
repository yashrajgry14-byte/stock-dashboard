import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta
import numpy as np
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Indian Stock Market Dashboard", layout="wide")
st.title("Indian Stock Market Dashboard")

indices = {
    "Nifty 50":        "^NSEI",
    "Nifty Bank":      "^NSEBANK",
    "Nifty Next 50":   "^NSMIDCP",
    "Nifty IT":        "^CNXIT",
    "Nifty Pharma":    "^CNXPHARMA",
    "Nifty FMCG":      "^CNXFMCG",
    "Nifty Metal":     "^CNXMETAL",
    "Nifty Auto":      "^CNXAUTO",
    "Nifty Realty":    "^CNXREALTY",
    "Nifty Energy":    "^CNXENERGY",
    "Nifty Infra":     "^CNXINFRA",
}
nifty500 = {
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
}

sector_peers = {
    "IT":        ["TCS.NS","INFY.NS","HCLTECH.NS","WIPRO.NS","TECHM.NS"],
    "Banking":   ["HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","AXISBANK.NS","KOTAKBANK.NS"],
    "FMCG":      ["HINDUNILVR.NS","ITC.NS","NESTLEIND.NS","DABUR.NS","MARICO.NS"],
    "Auto":      ["MARUTI.NS","TATAMOTORS.NS","BAJAJ-AUTO.NS","HEROMOTOCO.NS","EICHERMOT.NS"],
    "Pharma":    ["SUNPHARMA.NS","DRREDDY.NS","CIPLA.NS","DIVISLAB.NS","LUPIN.NS"],
    "Metal":     ["TATASTEEL.NS","JSWSTEEL.NS","HINDALCO.NS","VEDL.NS","COALINDIA.NS"],
    "Oil & Gas": ["RELIANCE.NS","ONGC.NS","IOC.NS","BPCL.NS","TATAPOWER.NS"],
    "Cement":    ["ULTRACEMCO.NS","SHREECEM.NS","AMBUJACEM.NS","GRASIM.NS"],
}


@st.cache_data(ttl=300)
def get_index_change(tkr):
    try:
        df = yf.Ticker(tkr).history(period="2d")
        if len(df) < 2:
            return None
        change = ((df["Close"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2]) * 100
        price  = df["Close"].iloc[-1]
        return round(change, 2), round(price, 2)
    except:
        return None


@st.cache_data(ttl=300)
def load_data(tkr, period):
    df = yf.Ticker(tkr).history(period=period)
    df.index = pd.to_datetime(df.index)
    return df


@st.cache_data(ttl=3600)
def load_full_history(tkr):
    df = yf.Ticker(tkr).history(period="max")
    df.index = pd.to_datetime(df.index)
    return df


@st.cache_data(ttl=600)
def get_news(company_name, sector_name):
    all_articles = []
    queries = [
        f"{company_name} stock NSE",
        f"{company_name} results deal order",
        f"{sector_name} India" if sector_name else f"{company_name} India",
    ]
    for q in queries:
        try:
            url  = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=en-IN&gl=IN&ceid=IN:en"
            resp = requests.get(url, timeout=5)
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item")[:4]:
                title   = item.findtext("title",   "")
                link    = item.findtext("link",    "#")
                source  = item.findtext("source",  "")
                pubdate = item.findtext("pubDate", "")
                if title:
                    all_articles.append({
                        "title":   title,
                        "link":    link,
                        "source":  source,
                        "pubdate": pubdate[:16] if pubdate else ""
                    })
        except:
            continue
    seen, unique = set(), []
    for a in all_articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
    return unique[:12]


def categorise_news(title):
    t = title.lower()
    if any(k in t for k in ["deal","order","contract","partnership","acqui",
                              "merger","investment","wins","bags","secures"]):
        return "Deal / Order / Investment", "green"
    if any(k in t for k in ["results","profit","revenue","earnings",
                              "quarterly","annual","loss","margin","q1","q2","q3","q4"]):
        return "Earnings / Results", "blue"
    if any(k in t for k in ["sector","industry","policy","regulation",
                              "government","rbi","sebi","budget","tax","norm"]):
        return "Sector / Policy", "orange"
    if any(k in t for k in ["ceo","board","management","appoint",
                              "resign","stake","promoter","buyback","dividend"]):
        return "Corporate movement", "violet"
    return "General news", "gray"


def normalise(arr):
    mn, mx = arr.min(), arr.max()
    if mx == mn:
        return arr * 0
    return (arr - mn) / (mx - mn)


# ── SECTOR HEATMAP ────────────────────────────────────────────
cols = st.columns(len(indices))
for i, (name, tkr) in enumerate(indices.items()):
    result = get_index_change(tkr)
    with cols[i]:
        if result:
            change, price = result
            encoded = requests.utils.quote(name)
            st.markdown(
                f"[**{name}**](/index_detail?index={encoded})",
                unsafe_allow_html=False
            )
            color = "green" if change >= 0 else "red"
            arrow = "↑" if change >= 0 else "↓"
            st.markdown(
                f"<span style='font-size:20px;font-weight:500'>"
                f"₹{price:,.0f}</span>  \n"
                f"<span style='color:{color}'>{arrow} {change:+.2f}%</span>",
                unsafe_allow_html=True
            )
        else:
            st.metric(label=name, value="N/A", delta="")

# ── STOCK SEARCH ──────────────────────────────────────────────
st.subheader("Search any stock")
search_query = st.text_input(
    "Search",
    placeholder="Type company name or NSE ticker e.g. Reliance or RELIANCE.NS",
    label_visibility="collapsed"
)
if search_query:
    matches = {
        name: tkr for name, tkr in nifty500.items()
        if search_query.lower() in name.lower() or search_query.upper() in tkr.upper()
    }
    if matches:
        selected_search = st.selectbox("Matches", list(matches.keys()), label_visibility="collapsed")
        if st.button(f"View {selected_search}"):
            st.session_state["selected_stock"] = matches[selected_search]
            st.session_state["selected_name"]  = selected_search
            st.session_state["mode"]           = "Stock"
    else:
        st.caption("Not in list — will try ticker directly")
        if st.button("Search this ticker"):
            st.session_state["selected_stock"] = search_query.upper()
            st.session_state["selected_name"]  = search_query.upper()
            st.session_state["mode"]           = "Stock"

st.divider()

# ── SIDEBAR ───────────────────────────────────────────────────
st.sidebar.header("Settings")
mode = st.sidebar.radio(
    "View", ["Index", "Stock"],
    index=0 if st.session_state.get("mode", "Index") == "Index" else 1
)

if mode == "Index":
    selected_name = st.sidebar.selectbox("Select index", list(indices.keys()))
    ticker        = indices[selected_name]
    show_nifty    = False
else:
    default_name  = st.session_state.get("selected_name", "Reliance Industries")
    stock_names   = list(nifty500.keys())
    default_idx   = stock_names.index(default_name) if default_name in stock_names else 0
    selected_name = st.sidebar.selectbox("Select company", stock_names, index=default_idx)
    ticker        = nifty500[selected_name]
    show_nifty    = st.sidebar.checkbox("Compare with Nifty 50", value=True)

period = st.sidebar.selectbox("Time period", ["1mo","3mo","6mo","1y","2y"])

# ── FETCH DATA ────────────────────────────────────────────────
df = load_data(ticker, period)
if df.empty:
    st.error(f"No data found for '{ticker}'.")
    st.stop()

df["MA_20"]    = df["Close"].rolling(20).mean()
df["MA_50"]    = df["Close"].rolling(50).mean()
df["RSI"]      = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
bb             = ta.volatility.BollingerBands(df["Close"])
df["BB_Upper"] = bb.bollinger_hband()
df["BB_Lower"] = bb.bollinger_lband()

# ── KPI METRICS ───────────────────────────────────────────────
latest  = df["Close"].iloc[-1]
prev    = df["Close"].iloc[-2]
change  = ((latest - prev) / prev) * 100
high    = df["High"].max()
low     = df["Low"].min()
avg_vol = df["Volume"].mean()

st.subheader(selected_name)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Price",    f"₹{latest:,.2f}", f"{change:+.2f}%")
c2.metric("Period High",      f"₹{high:,.2f}")
c3.metric("Period Low",       f"₹{low:,.2f}")
c4.metric("Avg Daily Volume", f"{avg_vol:,.0f}")

st.divider()

# ── CANDLESTICK CHART ─────────────────────────────────────────
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    row_heights=[0.7, 0.3], vertical_spacing=0.05)

fig.add_trace(go.Candlestick(
    x=df.index, open=df["Open"], high=df["High"],
    low=df["Low"], close=df["Close"], name=selected_name
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=df["MA_20"],
    line=dict(color="royalblue", width=1.5), name="MA 20"
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=df["MA_50"],
    line=dict(color="orange", width=1.5), name="MA 50"
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=df["BB_Upper"],
    line=dict(color="gray", width=1, dash="dash"), name="BB Upper"
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df.index, y=df["BB_Lower"],
    line=dict(color="gray", width=1, dash="dash"),
    name="BB Lower", fill="tonexty", fillcolor="rgba(200,200,200,0.1)"
), row=1, col=1)
colors = ["green" if c >= o else "red" for c, o in zip(df["Close"], df["Open"])]
fig.add_trace(go.Bar(
    x=df.index, y=df["Volume"],
    marker_color=colors, name="Volume", opacity=0.6
), row=2, col=1)
fig.update_layout(
    title=f"{selected_name} — Price & Volume",
    xaxis_rangeslider_visible=False, height=600
)
fig.update_yaxes(title_text="Price (₹)", row=1, col=1)
fig.update_yaxes(title_text="Volume",    row=2, col=1)
st.plotly_chart(fig, use_container_width=True)

# ── NIFTY COMPARISON ──────────────────────────────────────────
if show_nifty:
    nifty_df = load_data("^NSEI", period)
    if not nifty_df.empty:
        stock_norm = (df["Close"] / df["Close"].iloc[0]) * 100
        nifty_norm = (nifty_df["Close"] / nifty_df["Close"].iloc[0]) * 100
        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Scatter(
            x=df.index, y=stock_norm,
            line=dict(color="royalblue", width=2), name=selected_name
        ))
        fig_cmp.add_trace(go.Scatter(
            x=nifty_df.index, y=nifty_norm,
            line=dict(color="orange", width=2, dash="dash"), name="Nifty 50"
        ))
        fig_cmp.update_layout(
            title=f"{selected_name} vs Nifty 50 (Normalised to 100)",
            height=350, yaxis_title="Indexed to 100"
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

# ── RSI CHART ─────────────────────────────────────────────────
st.subheader("RSI — Relative Strength Index (14)")
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(
    x=df.index, y=df["RSI"],
    line=dict(color="purple", width=2), name="RSI"
))
fig_rsi.add_hline(y=70, line_color="red",   line_dash="dash", annotation_text="Overbought (70)")
fig_rsi.add_hline(y=30, line_color="green", line_dash="dash", annotation_text="Oversold (30)")
fig_rsi.update_layout(height=300, yaxis=dict(range=[0, 100]))
st.plotly_chart(fig_rsi, use_container_width=True)

with st.expander("View raw data (last 30 days)"):
    st.dataframe(
        df[["Open","High","Low","Close","Volume"]].tail(30).round(2),
        use_container_width=True
    )

st.divider()

# ── PRICE HISTORY PERIOD SELECTOR ────────────────────────────
st.subheader(f"Price history — {selected_name}")
period_map = {
    "1 Month":  "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year":   "1y",
    "3 Years":  "3y",
    "5 Years":  "5y",
}
sel_period   = st.radio("Select period", list(period_map.keys()), horizontal=True, index=3)
chart_period = period_map[sel_period]
period_df    = load_data(ticker, chart_period)
history_df   = load_full_history(ticker)

if not period_df.empty:
    p_start  = period_df["Close"].iloc[0]
    p_end    = period_df["Close"].iloc[-1]
    p_change = ((p_end - p_start) / p_start) * 100
    lc = "green" if p_change >= 0 else "red"
    fc = "rgba(0,180,0,0.08)" if p_change >= 0 else "rgba(220,0,0,0.08)"
    fig_p = go.Figure()
    fig_p.add_trace(go.Scatter(
        x=period_df.index, y=period_df["Close"],
        fill="tozeroy", fillcolor=fc,
        line=dict(color=lc, width=2), name="Close"
    ))
    if len(period_df) >= 20:
        period_df["MA_20"] = period_df["Close"].rolling(20).mean()
        fig_p.add_trace(go.Scatter(
            x=period_df.index, y=period_df["MA_20"],
            line=dict(color="orange", width=1.5, dash="dash"), name="20-day MA"
        ))
    if len(period_df) >= 50:
        period_df["MA_50"] = period_df["Close"].rolling(50).mean()
        fig_p.add_trace(go.Scatter(
            x=period_df.index, y=period_df["MA_50"],
            line=dict(color="royalblue", width=1.5, dash="dot"), name="50-day MA"
        ))
    fig_p.update_layout(
        title=f"{selected_name} — {sel_period} ({p_change:+.2f}%)",
        height=420, yaxis_title="Price (₹)",
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig_p, use_container_width=True)

# ── MONTHLY RETURN BAR ────────────────────────────────────────
if len(history_df) > 200:
    st.subheader("Average return by calendar month")
    monthly_close = history_df["Close"].resample("ME").last()
    monthly_ret   = monthly_close.pct_change() * 100
    mdf           = monthly_ret.reset_index()
    mdf.columns   = ["Date", "Return"]
    mdf["Month"]  = mdf["Date"].dt.strftime("%b")
    month_order   = ["Jan","Feb","Mar","Apr","May","Jun",
                     "Jul","Aug","Sep","Oct","Nov","Dec"]
    avg_by_month  = mdf.groupby("Month")["Return"].mean().reindex(month_order).reset_index()
    avg_by_month.columns = ["Month", "Avg Return %"]
    bcolors = ["green" if x >= 0 else "red" for x in avg_by_month["Avg Return %"]]
    fig_mret = go.Figure(go.Bar(
        x=avg_by_month["Month"],
        y=avg_by_month["Avg Return %"].round(2),
        marker_color=bcolors
    ))
    fig_mret.update_layout(
        title="Average monthly return — full history",
        height=320, yaxis_title="Avg return %"
    )
    st.plotly_chart(fig_mret, use_container_width=True)
    st.caption("Shows which months have historically been strong or weak for this stock.")

# ── SIGNAL ANALYSIS ───────────────────────────────────────────
st.divider()
st.subheader("Signal analysis — pattern based")
st.caption("Finds similar historical price patterns and shows what happened next.")

if len(history_df) >= 100:
    current_window = 20
    recent_prices  = history_df["Close"].iloc[-current_window:].values
    current_norm   = normalise(recent_prices)
    closes         = history_df["Close"].values
    dates          = history_df.index
    similarities   = []
    search_end     = len(closes) - current_window - 60

    for i in range(current_window, search_end):
        hw   = closes[i - current_window: i]
        hn   = normalise(hw)
        dist = np.sqrt(np.mean((current_norm - hn) ** 2))
        similarities.append((i, dist))

    similarities.sort(key=lambda x: x[1])
    top_matches = similarities[:10]

    forward_30, forward_90 = [], []
    for idx, dist in top_matches:
        if idx + 30 < len(closes):
            forward_30.append(((closes[idx+30] - closes[idx]) / closes[idx]) * 100)
        if idx + 90 < len(closes):
            forward_90.append(((closes[idx+90] - closes[idx]) / closes[idx]) * 100)

    avg_30      = np.mean(forward_30) if forward_30 else 0
    avg_90      = np.mean(forward_90) if forward_90 else 0
    win_rate_30 = (sum(1 for r in forward_30 if r > 0) / len(forward_30) * 100) if forward_30 else 0
    win_rate_90 = (sum(1 for r in forward_90 if r > 0) / len(forward_90) * 100) if forward_90 else 0

    recent              = history_df.tail(252).copy()
    recent["MA_50"]     = recent["Close"].rolling(50).mean()
    recent["MA_200"]    = recent["Close"].rolling(200).mean()
    recent["RSI"]       = ta.momentum.RSIIndicator(recent["Close"], window=14).rsi()
    macd_ind            = ta.trend.MACD(recent["Close"])
    recent["MACD"]      = macd_ind.macd()
    recent["MACD_Sig"]  = macd_ind.macd_signal()

    price    = recent["Close"].iloc[-1]
    ma50     = recent["MA_50"].iloc[-1]
    ma200    = recent["MA_200"].iloc[-1]
    rsi      = recent["RSI"].iloc[-1]
    macd_val = recent["MACD"].iloc[-1]
    macd_sig = recent["MACD_Sig"].iloc[-1]

    week52_high    = recent["Close"].max()
    week52_low     = recent["Close"].min()
    momentum       = ((history_df["Close"].iloc[-1] - history_df["Close"].iloc[-current_window]) / history_df["Close"].iloc[-current_window]) * 100
    avg_vol_recent = history_df["Volume"].iloc[-5:].mean()
    avg_vol_30d    = history_df["Volume"].iloc[-30:].mean()
    vol_change     = ((avg_vol_recent - avg_vol_30d) / avg_vol_30d) * 100

    signals = []
    score   = 0

    if win_rate_30 >= 65:
        signals.append(("Pattern win rate",
            f"Similar past patterns led to gains {win_rate_30:.0f}% of the time over 30 days",
            "Bullish", "+"))
        score += 2
    elif win_rate_30 <= 35:
        signals.append(("Pattern win rate",
            f"Similar past patterns led to gains only {win_rate_30:.0f}% of the time over 30 days",
            "Bearish", "-"))
        score -= 2
    else:
        signals.append(("Pattern win rate",
            f"Mixed results — {win_rate_30:.0f}% positive over 30 days",
            "Neutral", "~"))

    if avg_30 > 3:
        signals.append(("30-day forward return",
            f"Stocks with this pattern returned +{avg_30:.1f}% over the next 30 days on average",
            "Bullish", "+"))
        score += 1
    elif avg_30 < -3:
        signals.append(("30-day forward return",
            f"Stocks with this pattern returned {avg_30:.1f}% over the next 30 days on average",
            "Bearish", "-"))
        score -= 1

    if avg_90 > 5:
        signals.append(("90-day forward return",
            f"Stocks with this pattern returned +{avg_90:.1f}% over the next 90 days on average",
            "Bullish", "+"))
        score += 1
    elif avg_90 < -5:
        signals.append(("90-day forward return",
            f"Stocks with this pattern returned {avg_90:.1f}% over the next 90 days on average",
            "Bearish", "-"))
        score -= 1

    if price > ma50:
        signals.append(("Price vs 50-day MA",
            "Price is above its 50-day moving average — short-term upward momentum",
            "Bullish", "+"))
        score += 1
    else:
        signals.append(("Price vs 50-day MA",
            "Price is below its 50-day moving average — short-term downward pressure",
            "Bearish", "-"))
        score -= 1

    if ma50 > ma200:
        signals.append(("Golden / Death cross",
            "50-day MA above 200-day MA (golden cross) — strong long-term bullish signal",
            "Bullish", "+"))
        score += 1
    else:
        signals.append(("Golden / Death cross",
            "50-day MA below 200-day MA (death cross) — long-term bearish signal",
            "Bearish", "-"))
        score -= 1

    if rsi < 35:
        signals.append(("RSI",
            f"RSI is {rsi:.1f} — oversold. Often signals a potential upward reversal",
            "Bullish", "+"))
        score += 1
    elif rsi > 65:
        signals.append(("RSI",
            f"RSI is {rsi:.1f} — overbought. Stock may be due for a pullback",
            "Bearish", "-"))
        score -= 1
    else:
        signals.append(("RSI",
            f"RSI is {rsi:.1f} — neutral zone, no strong signal",
            "Neutral", "~"))

    if macd_val > macd_sig:
        signals.append(("MACD",
            "MACD above signal line — positive and building momentum",
            "Bullish", "+"))
        score += 1
    else:
        signals.append(("MACD",
            "MACD below signal line — weakening or negative momentum",
            "Bearish", "-"))
        score -= 1

    if momentum > 5:
        signals.append(("20-day momentum",
            f"Stock moved +{momentum:.1f}% in last 20 trading days — strong recent trend",
            "Bullish", "+"))
        score += 1
    elif momentum < -5:
        signals.append(("20-day momentum",
            f"Stock moved {momentum:.1f}% in last 20 trading days — recent selling pressure",
            "Bearish", "-"))
        score -= 1
    else:
        signals.append(("20-day momentum",
            f"Stock moved {momentum:.1f}% in last 20 days — sideways / consolidating",
            "Neutral", "~"))

    if vol_change > 20:
        signals.append(("Volume trend",
            f"Volume up {vol_change:.0f}% vs 30-day average — rising volume confirms price moves",
            "Bullish", "+"))
        score += 1
    elif vol_change < -20:
        signals.append(("Volume trend",
            f"Volume down {abs(vol_change):.0f}% vs 30-day average — low volume weakens trend",
            "Bearish", "-"))
        score -= 1
    else:
        signals.append(("Volume trend",
            f"Volume close to average ({vol_change:+.0f}%) — no unusual activity",
            "Neutral", "~"))

    if score >= 6:
        verdict, vcolor = "Strongly Bullish", "green"
        summary = "Strong positive signals across pattern and technical analysis"
    elif score >= 3:
        verdict, vcolor = "Bullish", "green"
        summary = "More positive signals than negative — moderate bullish case"
    elif score <= -6:
        verdict, vcolor = "Strongly Bearish", "red"
        summary = "Strong negative signals across pattern and technical analysis"
    elif score <= -3:
        verdict, vcolor = "Bearish", "red"
        summary = "More negative signals than positive — moderate bearish case"
    else:
        verdict, vcolor = "Neutral / Mixed", "orange"
        summary = "Conflicting signals — no clear directional bias"

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        st.markdown("#### Technical & pattern signals")
        m1, m2 = st.columns(2)
        m1.metric("Pattern matches", len(top_matches))
        m2.metric("Win rate 30d",    f"{win_rate_30:.0f}%")
        m3, m4 = st.columns(2)
        m3.metric("Avg return 30d",  f"{avg_30:+.1f}%")
        m4.metric("Avg return 90d",  f"{avg_90:+.1f}%")

        st.markdown(f"### :{vcolor}[{verdict}]")
        st.caption(summary)
        st.markdown("---")

        fig_pat = go.Figure()
        fig_pat.add_trace(go.Scatter(
            y=current_norm,
            line=dict(color="white", width=3),
            name="Current 20-day pattern"
        ))
        for rank, (idx, dist) in enumerate(top_matches[:5]):
            hw = closes[idx - current_window: idx]
            fig_pat.add_trace(go.Scatter(
                y=normalise(hw),
                line=dict(width=1, dash="dot"),
                name=f"Match {rank+1}: {dates[idx].strftime('%b %Y')}"
            ))
        fig_pat.update_layout(
            title="Current pattern vs 5 most similar historical patterns",
            height=300, yaxis_title="Normalised price"
        )
        st.plotly_chart(fig_pat, use_container_width=True)

        st.markdown("**Signal breakdown:**")
        for factor, explanation, direction, sign in signals:
            if direction == "Bullish":
                st.markdown(f"**:green[{sign} {factor}]**")
            elif direction == "Bearish":
                st.markdown(f"**:red[{sign} {factor}]**")
            else:
                st.markdown(f"**:orange[{sign} {factor}]**")
            st.caption(explanation)

        st.info(
            "Pattern matching uses Euclidean distance to find similar 20-day "
            "price shapes in this stock's full history and measures what happened "
            "in the 30 and 90 days after. NOT financial advice."
        )

    with right_col:
        st.markdown("#### News & market events")
        st.caption("Recent news categorised by type — deals, earnings, policy, corporate moves.")

        try:
            info     = yf.Ticker(ticker).info
            sector   = info.get("sector",   "")
            industry = info.get("industry", "")
            if sector:
                st.caption(f"Sector: {sector} | Industry: {industry}")
        except:
            sector = ""

        news_items = get_news(selected_name, sector)

        if news_items:
            for item in news_items:
                category, color = categorise_news(item["title"])
                st.markdown(
                    f":{color}[**{category}**]  \n"
                    f"[{item['title']}]({item['link']})  \n"
                    f"<span style='font-size:11px;color:gray'>"
                    f"{item['source']} · {item['pubdate']}</span>",
                    unsafe_allow_html=True
                )
                st.markdown("---")
        else:
            st.info("No recent news found.")

        st.markdown("#### Sector peers today")
        peer_group       = []
        peer_sector_name = ""
        for sec, peers in sector_peers.items():
            if ticker in peers:
                peer_group       = [p for p in peers if p != ticker]
                peer_sector_name = sec
                break

        if peer_group:
            st.caption(f"{peer_sector_name} sector peers — click name to open on NSE")
            for peer_ticker in peer_group:
                peer_name = next(
                    (k for k, v in nifty500.items() if v == peer_ticker),
                    peer_ticker.replace(".NS", "")
                )
                result = get_index_change(peer_ticker)
                if result:
                    chg, pprice = result
                    arrow  = "↑" if chg >= 0 else "↓"
                    color  = "green" if chg >= 0 else "red"
                    symbol = peer_ticker.replace(".NS", "")
                    url    = f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}"
                    st.markdown(
                        f":{color}[{arrow}] [{peer_name}]({url}) — "
                        f"<span style='color:{'green' if chg>=0 else 'red'}'>"
                        f"₹{pprice:,.0f} ({chg:+.2f}%)</span>",
                        unsafe_allow_html=True
                    )
        else:
            st.caption("Peer data not available for this stock.")

            # ── STRATEGY BACKTESTING ENGINE ───────────────────────────────
st.divider()
st.subheader("Strategy backtesting engine")
st.caption("Test a trading strategy on this stock's full price history and see how it would have performed.")

if len(history_df) < 100:
    st.warning("Not enough data to backtest.")
else:
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

    @st.cache_data(ttl=3600)
    def load_bt_data(tkr, period):
        df = yf.Ticker(tkr).history(period=period)
        df.index = pd.to_datetime(df.index)
        return df.copy()

    bt_df = load_bt_data(ticker, period_lookup[bt_period])

    if bt_df.empty or len(bt_df) < 60:
        st.warning("Not enough data for this period.")
    else:
        bt_df = bt_df.copy()

        # ── GENERATE SIGNALS FOR CHOSEN STRATEGY ─────────────
        bt_df["Signal"] = 0  # 1 = buy, -1 = sell, 0 = hold

        if strategy == "MA Crossover (20/50)":
            bt_df["MA_fast"] = bt_df["Close"].rolling(20).mean()
            bt_df["MA_slow"] = bt_df["Close"].rolling(50).mean()
            bt_df["Signal"]  = np.where(
                bt_df["MA_fast"] > bt_df["MA_slow"], 1, -1
            )
            strategy_desc = (
                "Buys when the 20-day MA crosses above the 50-day MA "
                "(short-term momentum stronger than medium-term). "
                "Sells when the 20-day MA crosses below the 50-day MA."
            )

        elif strategy == "MA Crossover (50/200)":
            bt_df["MA_fast"] = bt_df["Close"].rolling(50).mean()
            bt_df["MA_slow"] = bt_df["Close"].rolling(200).mean()
            bt_df["Signal"]  = np.where(
                bt_df["MA_fast"] > bt_df["MA_slow"], 1, -1
            )
            strategy_desc = (
                "Classic golden cross / death cross strategy. Buys when "
                "50-day MA crosses above 200-day MA and sells when it crosses below. "
                "Slower to react but filters out noise."
            )

        elif strategy == "RSI Strategy (30/70)":
            bt_df["RSI"] = ta.momentum.RSIIndicator(
                bt_df["Close"], window=14
            ).rsi()
            bt_df["Signal"] = 0
            bt_df.loc[bt_df["RSI"] < 30, "Signal"] =  1
            bt_df.loc[bt_df["RSI"] > 70, "Signal"] = -1
            strategy_desc = (
                "Buys when RSI drops below 30 (oversold — stock may be undervalued). "
                "Sells when RSI rises above 70 (overbought — stock may be overvalued). "
                "Works best in sideways markets."
            )

        elif strategy == "MACD Crossover":
            macd_bt         = ta.trend.MACD(bt_df["Close"])
            bt_df["MACD"]   = macd_bt.macd()
            bt_df["MACD_S"] = macd_bt.macd_signal()
            bt_df["Signal"] = np.where(
                bt_df["MACD"] > bt_df["MACD_S"], 1, -1
            )
            strategy_desc = (
                "Buys when the MACD line crosses above its signal line "
                "(momentum turning positive). Sells when MACD crosses below "
                "its signal line (momentum turning negative)."
            )

        elif strategy == "Bollinger Band Bounce":
            bb_bt              = ta.volatility.BollingerBands(bt_df["Close"])
            bt_df["BB_upper"]  = bb_bt.bollinger_hband()
            bt_df["BB_lower"]  = bb_bt.bollinger_lband()
            bt_df["Signal"]    = 0
            bt_df.loc[bt_df["Close"] < bt_df["BB_lower"], "Signal"] =  1
            bt_df.loc[bt_df["Close"] > bt_df["BB_upper"], "Signal"] = -1
            strategy_desc = (
                "Buys when price touches or falls below the lower Bollinger Band "
                "(price statistically low relative to recent volatility). "
                "Sells when price touches or exceeds the upper band."
            )

        # ── RUN THE BACKTEST ──────────────────────────────────
        bt_df = bt_df.dropna()
        capital      = float(initial_capital)
        shares       = 0.0
        in_trade     = False
        buy_price    = 0.0
        trades       = []
        portfolio    = []
        prev_signal  = 0

        for i, row in bt_df.iterrows():
            sig = row["Signal"]
            price_now = row["Close"]

            # Detect signal change — only act on crossovers
            if sig == 1 and prev_signal != 1 and not in_trade:
                shares    = capital / price_now
                capital   = 0.0
                buy_price = price_now
                in_trade  = True
                trades.append({
                    "Date":   i,
                    "Type":   "BUY",
                    "Price":  round(price_now, 2),
                    "Shares": round(shares, 4)
                })

            elif sig == -1 and prev_signal != -1 and in_trade:
                capital  = shares * price_now
                profit   = capital - (shares * buy_price)
                in_trade = False
                trades.append({
                    "Date":    i,
                    "Type":    "SELL",
                    "Price":   round(price_now, 2),
                    "Shares":  round(shares, 4),
                    "Profit":  round(profit, 2),
                    "Return%": round((price_now - buy_price) / buy_price * 100, 2)
                })
                shares = 0.0

            prev_signal = sig
            # Portfolio value at this point
            port_value = capital + shares * price_now
            portfolio.append({"Date": i, "Value": port_value})

        # Close open trade at end
        if in_trade:
            final_price = bt_df["Close"].iloc[-1]
            capital     = shares * final_price
            profit      = capital - (shares * buy_price)
            trades.append({
                "Date":    bt_df.index[-1],
                "Type":    "SELL (end)",
                "Price":   round(final_price, 2),
                "Shares":  round(shares, 4),
                "Profit":  round(profit, 2),
                "Return%": round((final_price - buy_price) / buy_price * 100, 2)
            })

        port_df       = pd.DataFrame(portfolio).set_index("Date")
        final_value   = port_df["Value"].iloc[-1]
        total_return  = ((final_value - initial_capital) / initial_capital) * 100

        # Buy and hold comparison
        bh_shares      = initial_capital / bt_df["Close"].iloc[0]
        bh_final       = bh_shares * bt_df["Close"].iloc[-1]
        bh_return      = ((bh_final - initial_capital) / initial_capital) * 100

        # Nifty buy and hold
        nifty_bt = load_bt_data("^NSEI", period_lookup[bt_period])
        if not nifty_bt.empty:
            nifty_shares  = initial_capital / nifty_bt["Close"].iloc[0]
            nifty_final   = nifty_shares * nifty_bt["Close"].iloc[-1]
            nifty_return  = ((nifty_final - initial_capital) / initial_capital) * 100
        else:
            nifty_return  = 0.0

        # Win rate
        sell_trades  = [t for t in trades if "Return%" in t]
        winning      = [t for t in sell_trades if t["Return%"] > 0]
        win_rate_bt  = (len(winning) / len(sell_trades) * 100) if sell_trades else 0

        # Max drawdown
        rolling_max  = port_df["Value"].cummax()
        drawdown     = (port_df["Value"] - rolling_max) / rolling_max * 100
        max_drawdown = drawdown.min()

        # Sharpe ratio (annualised, assume 0% risk free)
        port_df["Daily_Return"] = port_df["Value"].pct_change()
        sharpe = (
            port_df["Daily_Return"].mean() /
            port_df["Daily_Return"].std() * np.sqrt(252)
        ) if port_df["Daily_Return"].std() > 0 else 0

        # ── STRATEGY EXPLANATION ──────────────────────────────
        st.markdown(f"**How this strategy works:** {strategy_desc}")
        st.divider()

        # ── KPI ROW ───────────────────────────────────────────
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("Final value",
                  f"₹{final_value:,.0f}",
                  f"{total_return:+.1f}%")
        k2.metric("Buy & hold return",
                  f"₹{bh_final:,.0f}",
                  f"{bh_return:+.1f}%")
        k3.metric("Nifty 50 return",
                  f"₹{nifty_final:,.0f}" if not nifty_bt.empty else "N/A",
                  f"{nifty_return:+.1f}%")
        k4.metric("Total trades",    len(sell_trades))
        k5.metric("Win rate",        f"{win_rate_bt:.0f}%")
        k6.metric("Max drawdown",    f"{max_drawdown:.1f}%")

        m1, m2 = st.columns(2)
        m1.metric("Sharpe ratio",
                  f"{sharpe:.2f}",
                  "Good > 1.0 | Great > 2.0")
        m2.metric("Strategy vs buy & hold",
                  f"{total_return - bh_return:+.1f}%",
                  "Positive = strategy beat holding")

        # ── PORTFOLIO VALUE CHART ─────────────────────────────
        fig_bt = go.Figure()

        fig_bt.add_trace(go.Scatter(
            x=port_df.index, y=port_df["Value"],
            line=dict(color="royalblue", width=2),
            name=f"{strategy} portfolio"
        ))

        # Buy and hold line
        bh_values = bh_shares * bt_df["Close"]
        fig_bt.add_trace(go.Scatter(
            x=bt_df.index, y=bh_values,
            line=dict(color="orange", width=1.5, dash="dash"),
            name=f"{selected_name} buy & hold"
        ))

        # Nifty line
        if not nifty_bt.empty:
            nifty_values = nifty_shares * nifty_bt["Close"]
            fig_bt.add_trace(go.Scatter(
                x=nifty_bt.index, y=nifty_values,
                line=dict(color="gray", width=1.5, dash="dot"),
                name="Nifty 50 buy & hold"
            ))

        # Mark buy signals on chart
        buy_dates  = [t["Date"] for t in trades if t["Type"] == "BUY"]
        buy_prices = [initial_capital] * len(buy_dates)
        for bd in buy_dates:
            if bd in port_df.index:
                buy_prices[buy_dates.index(bd)] = port_df.loc[bd, "Value"]

        fig_bt.add_trace(go.Scatter(
            x=buy_dates, y=buy_prices,
            mode="markers",
            marker=dict(color="green", size=10, symbol="triangle-up"),
            name="Buy signal"
        ))

        sell_dates  = [t["Date"] for t in trades if "SELL" in t["Type"]]
        sell_prices = []
        for sd in sell_dates:
            if sd in port_df.index:
                sell_prices.append(port_df.loc[sd, "Value"])
            else:
                sell_prices.append(final_value)

        fig_bt.add_trace(go.Scatter(
            x=sell_dates, y=sell_prices,
            mode="markers",
            marker=dict(color="red", size=10, symbol="triangle-down"),
            name="Sell signal"
        ))

        fig_bt.update_layout(
            title=f"{strategy} — Portfolio value over time vs benchmarks",
            height=500,
            yaxis_title="Portfolio value (₹)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_bt, use_container_width=True)

        # ── DRAWDOWN CHART ────────────────────────────────────
        fig_dd = go.Figure()
        fig_dd.add_trace(go.Scatter(
            x=drawdown.index, y=drawdown.values,
            fill="tozeroy",
            fillcolor="rgba(220,0,0,0.15)",
            line=dict(color="red", width=1),
            name="Drawdown %"
        ))
        fig_dd.update_layout(
            title="Drawdown over time — how far below peak at each point",
            height=250,
            yaxis_title="Drawdown %"
        )
        st.plotly_chart(fig_dd, use_container_width=True)

        # ── TRADE LOG ─────────────────────────────────────────
        with st.expander(f"Full trade log ({len(sell_trades)} completed trades)"):
            if sell_trades:
                trades_df = pd.DataFrame(sell_trades)
                trades_df["Date"] = pd.to_datetime(trades_df["Date"]).dt.strftime("%d %b %Y")
                st.dataframe(trades_df, use_container_width=True)
                avg_return = np.mean([t["Return%"] for t in sell_trades])
                best_trade = max(sell_trades, key=lambda t: t["Return%"])
                worst_trade = min(sell_trades, key=lambda t: t["Return%"])
                tc1, tc2, tc3 = st.columns(3)
                tc1.metric("Avg return per trade", f"{avg_return:+.2f}%")
                tc2.metric("Best trade",  f"+{best_trade['Return%']:.1f}%",
                           best_trade["Date"].strftime("%b %Y") if hasattr(best_trade["Date"], "strftime") else "")
                tc3.metric("Worst trade", f"{worst_trade['Return%']:.1f}%",
                           worst_trade["Date"].strftime("%b %Y") if hasattr(worst_trade["Date"], "strftime") else "")
            else:
                st.info("No completed trades in this period.")

        st.info(
            "Backtesting shows how a strategy would have performed historically. "
            "Past performance does not guarantee future results. "
            "This does not account for brokerage fees, taxes, or slippage. "
            "NOT financial advice."
        )

st.caption("Data from Yahoo Finance via yfinance. Prices in INR. Not financial advice.")
