import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import requests
import xml.etree.ElementTree as ET
import numpy as np

st.set_page_config(page_title="Index Detail", layout="wide")

# ── INDEX CONSTITUENTS ────────────────────────────────────────
index_stocks = {
    "Nifty 50": {
        "ticker": "^NSEI",
        "stocks": {
            "Reliance Industries": "RELIANCE.NS",
            "TCS":                 "TCS.NS",
            "HDFC Bank":           "HDFCBANK.NS",
            "Infosys":             "INFY.NS",
            "ICICI Bank":          "ICICIBANK.NS",
            "Hindustan Unilever":  "HINDUNILVR.NS",
            "ITC":                 "ITC.NS",
            "Kotak Mahindra Bank": "KOTAKBANK.NS",
            "Larsen & Toubro":     "LT.NS",
            "Axis Bank":           "AXISBANK.NS",
            "State Bank of India": "SBIN.NS",
            "Bajaj Finance":       "BAJFINANCE.NS",
            "Bharti Airtel":       "BHARTIARTL.NS",
            "Asian Paints":        "ASIANPAINT.NS",
            "Maruti Suzuki":       "MARUTI.NS",
            "HCL Technologies":    "HCLTECH.NS",
            "Sun Pharma":          "SUNPHARMA.NS",
            "Titan Company":       "TITAN.NS",
            "Wipro":               "WIPRO.NS",
            "Ultratech Cement":    "ULTRACEMCO.NS",
            "NTPC":                "NTPC.NS",
            "Power Grid":          "POWERGRID.NS",
            "Tech Mahindra":       "TECHM.NS",
            "Bajaj Finserv":       "BAJAJFINSV.NS",
            "Adani Ports":         "ADANIPORTS.NS",
            "Tata Motors":         "TATAMOTORS.NS",
            "JSW Steel":           "JSWSTEEL.NS",
            "Tata Steel":          "TATASTEEL.NS",
            "Dr Reddy's":          "DRREDDY.NS",
            "Cipla":               "CIPLA.NS",
            "Eicher Motors":       "EICHERMOT.NS",
            "Hero MotoCorp":       "HEROMOTOCO.NS",
            "Bajaj Auto":          "BAJAJ-AUTO.NS",
            "Grasim Industries":   "GRASIM.NS",
            "IndusInd Bank":       "INDUSINDBK.NS",
            "Hindalco":            "HINDALCO.NS",
            "Coal India":          "COALINDIA.NS",
            "ONGC":                "ONGC.NS",
            "Tata Consumer":       "TATACONSUM.NS",
            "Dmart":               "DMART.NS",
        }
    },
    "Nifty Bank": {
        "ticker": "^NSEBANK",
        "stocks": {
            "HDFC Bank":           "HDFCBANK.NS",
            "ICICI Bank":          "ICICIBANK.NS",
            "Kotak Mahindra Bank": "KOTAKBANK.NS",
            "Axis Bank":           "AXISBANK.NS",
            "State Bank of India": "SBIN.NS",
            "IndusInd Bank":       "INDUSINDBK.NS",
            "Bank of Baroda":      "BANKBARODA.NS",
            "Punjab National Bank":"PNB.NS",
            "Federal Bank":        "FEDERALBNK.NS",
            "AU Small Finance":    "AUBANK.NS",
        }
    },
    "Nifty IT": {
        "ticker": "^CNXIT",
        "stocks": {
            "TCS":              "TCS.NS",
            "Infosys":          "INFY.NS",
            "HCL Technologies": "HCLTECH.NS",
            "Wipro":            "WIPRO.NS",
            "Tech Mahindra":    "TECHM.NS",
            "LTIMindtree":      "LTIM.NS",
            "Mphasis":          "MPHASIS.NS",
            "Persistent":       "PERSISTENT.NS",
            "Coforge":          "COFORGE.NS",
            "Hexaware":         "HEXAWARE.NS",
        }
    },
    "Nifty Pharma": {
        "ticker": "^CNXPHARMA",
        "stocks": {
            "Sun Pharma":      "SUNPHARMA.NS",
            "Dr Reddy's":      "DRREDDY.NS",
            "Cipla":           "CIPLA.NS",
            "Divis Lab":       "DIVISLAB.NS",
            "Lupin":           "LUPIN.NS",
            "Aurobindo":       "AUROPHARMA.NS",
            "Biocon":          "BIOCON.NS",
            "Torrent Pharma":  "TORNTPHARM.NS",
            "Mankind Pharma":  "MANKIND.NS",
            "Alkem Labs":      "ALKEM.NS",
        }
    },
    "Nifty FMCG": {
        "ticker": "^CNXFMCG",
        "stocks": {
            "Hindustan Unilever": "HINDUNILVR.NS",
            "ITC":                "ITC.NS",
            "Nestle India":       "NESTLEIND.NS",
            "Dabur India":        "DABUR.NS",
            "Marico":             "MARICO.NS",
            "Godrej Consumer":    "GODREJCP.NS",
            "Colgate":            "COLPAL.NS",
            "Britannia":          "BRITANNIA.NS",
            "Varun Beverages":    "VBL.NS",
            "Tata Consumer":      "TATACONSUM.NS",
        }
    },
    "Nifty Metal": {
        "ticker": "^CNXMETAL",
        "stocks": {
            "Tata Steel":     "TATASTEEL.NS",
            "JSW Steel":      "JSWSTEEL.NS",
            "Hindalco":       "HINDALCO.NS",
            "Vedanta":        "VEDL.NS",
            "Coal India":     "COALINDIA.NS",
            "SAIL":           "SAIL.NS",
            "NMDC":           "NMDC.NS",
            "Jindal Steel":   "JINDALSTEL.NS",
            "APL Apollo":     "APLAPOLLO.NS",
            "Welspun Corp":   "WELCORP.NS",
        }
    },
    "Nifty Auto": {
        "ticker": "^CNXAUTO",
        "stocks": {
            "Maruti Suzuki": "MARUTI.NS",
            "Tata Motors":   "TATAMOTORS.NS",
            "Bajaj Auto":    "BAJAJ-AUTO.NS",
            "Hero MotoCorp": "HEROMOTOCO.NS",
            "Eicher Motors": "EICHERMOT.NS",
            "TVS Motor":     "TVSMOTOR.NS",
            "Ashok Leyland": "ASHOKLEY.NS",
            "Motherson":     "MOTHERSON.NS",
            "Bosch":         "BOSCHLTD.NS",
            "MRF":           "MRF.NS",
        }
    },
    "Nifty Realty": {
        "ticker": "^CNXREALTY",
        "stocks": {
            "DLF":             "DLF.NS",
            "Godrej Properties":"GODREJPROP.NS",
            "Oberoi Realty":   "OBEROIRLTY.NS",
            "Prestige Estates":"PRESTIGE.NS",
            "Phoenix Mills":   "PHOENIXLTD.NS",
            "Macrotech":       "LODHA.NS",
            "Sobha":           "SOBHA.NS",
            "Brigade":         "BRIGADE.NS",
        }
    },
    "Nifty Energy": {
        "ticker": "^CNXENERGY",
        "stocks": {
            "Reliance Industries": "RELIANCE.NS",
            "ONGC":                "ONGC.NS",
            "Power Grid":          "POWERGRID.NS",
            "NTPC":                "NTPC.NS",
            "IOC":                 "IOC.NS",
            "BPCL":                "BPCL.NS",
            "Tata Power":          "TATAPOWER.NS",
            "Adani Green":         "ADANIGREEN.NS",
            "Adani Power":         "ADANIPOWER.NS",
            "GAIL":                "GAIL.NS",
        }
    },
    "Nifty Infra": {
        "ticker": "^CNXINFRA",
        "stocks": {
            "Larsen & Toubro":  "LT.NS",
            "Power Grid":       "POWERGRID.NS",
            "NTPC":             "NTPC.NS",
            "Adani Ports":      "ADANIPORTS.NS",
            "Bharti Airtel":    "BHARTIARTL.NS",
            "Tata Communications": "TATACOMM.NS",
            "GMR Airports":     "GMRINFRA.NS",
            "IRB Infra":        "IRB.NS",
            "KNR Constructions":"KNRCON.NS",
            "PNC Infratech":    "PNCINFRA.NS",
        }
    },
    "Nifty Next 50": {
        "ticker": "^NSMIDCP",
        "stocks": {
            "Adani Enterprises":  "ADANIENT.NS",
            "Vedanta":            "VEDL.NS",
            "Zomato":             "ZOMATO.NS",
            "Trent":              "TRENT.NS",
            "HAL":                "HAL.NS",
            "IRCTC":              "IRCTC.NS",
            "LIC India":          "LICI.NS",
            "SBI Life":           "SBILIFE.NS",
            "HDFC Life":          "HDFCLIFE.NS",
            "Pidilite":           "PIDILITIND.NS",
            "Havells":            "HAVELLS.NS",
            "Siemens":            "SIEMENS.NS",
            "Dmart":              "DMART.NS",
            "Muthoot Finance":    "MUTHOOTFIN.NS",
            "Shree Cement":       "SHREECEM.NS",
        }
    },
}

# ── HELPER FUNCTIONS ──────────────────────────────────────────
@st.cache_data(ttl=300)
def get_stock_change(tkr):
    try:
        df = yf.Ticker(tkr).history(period="2d")
        if len(df) < 2:
            return None
        change = ((df["Close"].iloc[-1] - df["Close"].iloc[-2]) /
                  df["Close"].iloc[-2]) * 100
        price  = df["Close"].iloc[-1]
        mkt_cap = yf.Ticker(tkr).info.get("marketCap", 0)
        return round(change, 2), round(price, 2), mkt_cap
    except:
        return None

@st.cache_data(ttl=300)
def load_index_history(tkr, period):
    df = yf.Ticker(tkr).history(period=period)
    df.index = pd.to_datetime(df.index)
    return df

@st.cache_data(ttl=600)
def get_sector_news(index_name):
    all_articles = []
    queries = [
        f"{index_name} India stocks",
        f"{index_name} sector India news",
        f"NSE {index_name} today",
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
    return unique[:10]

def categorise_news(title):
    t = title.lower()
    if any(k in t for k in ["policy","regulation","rbi","sebi","budget","tax","norm","rule"]):
        return "Policy / Regulation", "orange"
    if any(k in t for k in ["results","profit","revenue","earnings","quarterly","loss"]):
        return "Earnings / Results", "blue"
    if any(k in t for k in ["deal","order","contract","merger","investment","acquisition"]):
        return "Deal / Investment", "green"
    if any(k in t for k in ["crash","fall","drop","slump","sell","bearish","weak"]):
        return "Market movement", "red"
    if any(k in t for k in ["rally","rise","gain","surge","bullish","strong","record"]):
        return "Market movement", "green"
    return "General", "gray"

# ── PAGE ──────────────────────────────────────────────────────
selected_index = st.query_params.get("index", "Nifty 50")

if selected_index not in index_stocks:
    selected_index = "Nifty 50"

index_info = index_stocks[selected_index]
index_tkr  = index_info["ticker"]
stocks     = index_info["stocks"]

st.title(f"{selected_index} — Index Detail")
st.markdown(f"[← Back to dashboard](/)")

# ── TIME PERIOD SELECTOR ──────────────────────────────────────
period_map = {
    "1 Month": "1mo", "3 Months": "3mo", "6 Months": "6mo",
    "1 Year": "1y", "3 Years": "3y", "5 Years": "5y"
}
sel_period   = st.radio("Time period", list(period_map.keys()),
                         horizontal=True, index=3)
chart_period = period_map[sel_period]

# ── INDEX CHART ───────────────────────────────────────────────
index_df = load_index_history(index_tkr, chart_period)

if not index_df.empty:
    p_start  = index_df["Close"].iloc[0]
    p_end    = index_df["Close"].iloc[-1]
    p_change = ((p_end - p_start) / p_start) * 100
    lc = "green" if p_change >= 0 else "red"
    fc = "rgba(0,180,0,0.08)" if p_change >= 0 else "rgba(220,0,0,0.08)"

    latest  = index_df["Close"].iloc[-1]
    prev    = index_df["Close"].iloc[-2]
    day_chg = ((latest - prev) / prev) * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current level",   f"{latest:,.2f}", f"{day_chg:+.2f}%")
    c2.metric("Period high",     f"{index_df['High'].max():,.2f}")
    c3.metric("Period low",      f"{index_df['Low'].min():,.2f}")
    c4.metric("Period return",   f"{p_change:+.2f}%")

    fig_idx = go.Figure()
    fig_idx.add_trace(go.Scatter(
        x=index_df.index, y=index_df["Close"],
        fill="tozeroy", fillcolor=fc,
        line=dict(color=lc, width=2), name=selected_index
    ))
    if len(index_df) >= 20:
        index_df["MA_20"] = index_df["Close"].rolling(20).mean()
        fig_idx.add_trace(go.Scatter(
            x=index_df.index, y=index_df["MA_20"],
            line=dict(color="orange", width=1.5, dash="dash"), name="20-day MA"
        ))
    if len(index_df) >= 50:
        index_df["MA_50"] = index_df["Close"].rolling(50).mean()
        fig_idx.add_trace(go.Scatter(
            x=index_df.index, y=index_df["MA_50"],
            line=dict(color="royalblue", width=1.5, dash="dot"), name="50-day MA"
        ))
    fig_idx.update_layout(
        title=f"{selected_index} — {sel_period} ({p_change:+.2f}%)",
        height=420, yaxis_title="Index level",
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig_idx, use_container_width=True)

st.divider()

# ── CONSTITUENT HEATMAP ───────────────────────────────────────
st.subheader("Constituent stocks — today's performance")
st.caption("Size = approximate market cap weight. Color = today's % change.")

stock_data = []
for name, tkr in stocks.items():
    result = get_stock_change(tkr)
    if result:
        change, price, mkt_cap = result
        stock_data.append({
            "name":    name,
            "ticker":  tkr,
            "change":  change,
            "price":   price,
            "mkt_cap": mkt_cap if mkt_cap else 1e10
        })

if stock_data:
    sdf = pd.DataFrame(stock_data)

    # Treemap heatmap
    fig_heat = go.Figure(go.Treemap(
        labels=[f"{r['name']}<br>{r['change']:+.2f}%"
                for _, r in sdf.iterrows()],
        parents=[""] * len(sdf),
        values=sdf["mkt_cap"],
        customdata=np.column_stack([
            sdf["change"], sdf["price"], sdf["ticker"]
        ]),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Price: ₹%{customdata[1]}<br>"
            "Change: %{customdata[0]:+.2f}%<br>"
            "<extra></extra>"
        ),
        marker=dict(
            colors=sdf["change"],
            colorscale=[
                [0.0, "#7f0000"],
                [0.3, "#cc0000"],
                [0.45, "#660000"],
                [0.5, "#333333"],
                [0.55, "#006600"],
                [0.7, "#00aa00"],
                [1.0, "#007700"],
            ],
            cmid=0,
            showscale=True,
            colorbar=dict(title="% Change")
        ),
        textfont=dict(size=13)
    ))
    fig_heat.update_layout(
        title=f"{selected_index} constituent heatmap — today",
        height=500,
        margin=dict(t=50, l=10, r=10, b=10)
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── STOCK TABLE ───────────────────────────────────────────
    st.subheader("All constituents")
    cols = st.columns(4)
    for i, row in sdf.sort_values("change", ascending=False).iterrows():
        col      = cols[i % 4]
        color    = "green" if row["change"] >= 0 else "red"
        arrow    = "↑" if row["change"] >= 0 else "↓"
        symbol   = row["ticker"].replace(".NS", "")

        encoded_ticker = requests.utils.quote(row["ticker"])
        encoded_index  = requests.utils.quote(selected_index)
        detail_url     = f"/stock_detail?ticker={encoded_ticker}&from={encoded_index}"
        with col:
                st.markdown(
                    f":{color}[{arrow}] [{row['name']}]({detail_url})  \n"
                    f"<span style='font-size:12px'>₹{row['price']:,.2f} "
                    f"({row['change']:+.2f}%)</span>",
                    unsafe_allow_html=True
                )

st.divider()

# ── NEWS & IMPACT ANALYSIS ────────────────────────────────────
st.subheader(f"News & sector impact — {selected_index}")

news_col, impact_col = st.columns([3, 2])

with news_col:
    st.markdown("#### Latest news")
    news_items = get_sector_news(selected_index)
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

with impact_col:
    st.markdown("#### How news types impact this sector")
    impact_map = {
        "Nifty Bank": {
            "RBI rate cut":       "Positive — lower rates boost lending margins",
            "RBI rate hike":      "Negative — compresses net interest margins",
            "NPA / bad loans":    "Negative — increases provisioning requirements",
            "Credit growth data": "Positive if strong — signals rising loan demand",
            "Budget / fiscal":    "Mixed — depends on capital allocation to PSU banks",
        },
        "Nifty IT": {
            "US recession fears":   "Negative — IT revenue heavily US-dependent",
            "Rupee depreciation":   "Positive — USD earnings worth more in INR",
            "Rupee appreciation":   "Negative — reduces INR value of exports",
            "AI / tech spending":   "Positive — drives demand for IT services",
            "US visa restrictions": "Negative — raises cost of offshore delivery",
        },
        "Nifty Pharma": {
            "USFDA approval":        "Positive — opens US generic drug market",
            "USFDA warning letter":  "Negative — bans exports from that facility",
            "Drug price controls":   "Negative — compresses domestic margins",
            "API supply chain":      "Risk — China dependency for raw materials",
            "R&D pipeline news":     "Positive if strong data released",
        },
        "Nifty FMCG": {
            "Rural consumption data": "Positive if strong — FMCG is rural-driven",
            "Input cost inflation":   "Negative — palm oil, crude impact margins",
            "Input cost deflation":   "Positive — boosts gross margins",
            "GST changes":            "Mixed — depends on product category",
            "Monsoon forecast":       "Positive if good — drives rural demand",
        },
        "Nifty Metal": {
            "China stimulus":        "Positive — China drives global metal demand",
            "US tariffs on steel":   "Mixed — protects domestic but hurts exporters",
            "Iron ore prices":       "Inverse — higher ore = higher input cost",
            "Infrastructure spend":  "Positive — government capex boosts demand",
            "Coal prices":           "Negative if high — raises energy cost",
        },
        "Nifty Auto": {
            "EV policy announcement": "Mixed — disrupts ICE, boosts EV players",
            "Fuel price changes":     "Inverse — high fuel hurts vehicle sales",
            "Credit / EMI rates":     "Negative if high — dampens retail purchases",
            "Monthly sales data":     "Positive if beats estimates",
            "Chip shortage":          "Negative — delays production",
        },
        "Nifty Energy": {
            "Crude oil price rise":   "Mixed — good for ONGC, bad for OMCs",
            "Renewable targets":      "Positive for Adani Green, Tata Power",
            "Gas price revision":     "Positive for upstream producers",
            "Subsidy burden":         "Negative for IOC, BPCL margins",
            "Geopolitical tensions":  "Volatile — crude price sensitivity",
        },
        "Nifty Realty": {
            "RBI rate cut":          "Positive — lower home loan EMIs boost demand",
            "RBI rate hike":         "Negative — higher EMIs slow home purchases",
            "New launch data":       "Positive if sales strong in metros",
            "RERA compliance news":  "Positive long term — builds buyer trust",
            "Commercial vacancy":    "Negative if rising — signals weak demand",
        },
    }

    sector_impacts = impact_map.get(selected_index, {
        "Government policy":   "Monitor for sector-specific regulation changes",
        "Global market moves": "Indian indices track global sentiment closely",
        "Earnings season":     "Watch for quarterly result beats or misses",
        "FII / DII flows":     "Heavy FII selling creates short-term pressure",
        "Rupee movement":      "Impacts export-heavy sectors significantly",
    })

    for event, impact in sector_impacts.items():
        color = "green" if any(w in impact.lower() for w in
                               ["positive","boost","strong","good"]) else \
                "red"   if any(w in impact.lower() for w in
                               ["negative","hurt","bad","weak","slow"]) else "orange"
        st.markdown(f"**{event}**")
        st.markdown(f":{color}[{impact}]")
        st.markdown("---")