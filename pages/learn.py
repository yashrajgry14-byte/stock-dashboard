import streamlit as st

st.set_page_config(page_title="Learn Stock Market", layout="wide")

st.title("Learn Stock Market")
st.caption("Everything you need to know before you start trading — explained simply.")

# ── NAVIGATION TABS ───────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Basics",
    "Chart Patterns",
    "Indicators",
    "Trading Styles",
    "Risk Management",
    "Indian Market"
])

# ══════════════════════════════════════════════════════════════
with tab1:
    st.header("Stock Market Basics")

    with st.expander("What is a stock?", expanded=True):
        st.markdown("""
A **stock** (also called a share or equity) represents a small piece of ownership in a company.

When a company wants to raise money, it splits itself into millions of tiny pieces and sells them to the public. Each piece is a stock. If you buy one share of Reliance Industries, you own a tiny fraction of Reliance.

**Why does the price go up or down?**
- If more people want to buy a stock than sell it → price goes up
- If more people want to sell than buy → price goes down
- This is driven by company performance, news, economy, global events

**Example:**
> TCS announces great quarterly results → investors get excited → more people buy → price rises
        """)

    with st.expander("What is NSE and BSE?"):
        st.markdown("""
India has two major stock exchanges:

**NSE — National Stock Exchange**
- India's largest exchange by volume
- Home of the Nifty 50 index
- Most stocks have `.NS` suffix on yfinance (e.g. RELIANCE.NS)

**BSE — Bombay Stock Exchange**
- Asia's oldest stock exchange (est. 1875)
- Home of the Sensex index (top 30 companies)
- `.BO` suffix on yfinance

**Which one to use?**
Most retail traders use NSE. Both exchanges list the same major companies at nearly identical prices.
        """)

    with st.expander("What is Nifty 50 and Sensex?"):
        st.markdown("""
These are **indices** — a basket of top stocks used to measure the overall market.

**Nifty 50**
- Top 50 companies listed on NSE by market cap
- Managed by NSE
- If Nifty goes up → most large Indian stocks went up

**Sensex**
- Top 30 companies listed on BSE
- Managed by BSE
- Older and more internationally recognised

**Think of it like this:**
> Nifty 50 is like the class average marks. If the class average is high, most students did well. If it's low, most struggled.

When people say "the market is up today" they usually mean Nifty 50 is up.
        """)

    with st.expander("What is Market Cap?"):
        st.markdown("""
**Market Capitalisation** = Current Share Price × Total Number of Shares

It tells you the total value of a company as priced by the market.

| Category | Market Cap | Examples |
|----------|-----------|---------|
| Large Cap | Above ₹20,000 Cr | Reliance, TCS, HDFC Bank |
| Mid Cap | ₹5,000 – ₹20,000 Cr | Voltas, Godrej Properties |
| Small Cap | Below ₹5,000 Cr | Smaller, lesser-known companies |

Large cap stocks are generally **safer but slower**. Small cap stocks are **riskier but can give higher returns**.
        """)

    with st.expander("What is an IPO?"):
        st.markdown("""
**IPO = Initial Public Offering**

When a private company sells its shares to the public for the very first time, it is called an IPO.

**Process:**
1. Company files papers with SEBI
2. Sets a price band (e.g. ₹70–₹72 per share)
3. Public applies for shares
4. Shares are allotted via lottery if oversubscribed
5. Stock lists on NSE/BSE and trading begins

**Example:** Zomato IPO in 2021 — price was ₹76. It listed at ₹115 on day one (a 51% gain for lucky allottees).

**Risk:** Not all IPOs go up. Many have listed below their issue price.
        """)

    with st.expander("What is a Dividend?"):
        st.markdown("""
A **dividend** is a portion of a company's profit that it shares with its shareholders.

**Example:**
> ITC announces a dividend of ₹6.50 per share.
> If you hold 100 shares, you receive ₹650 in your bank account.

**Dividend Yield** = (Annual Dividend / Share Price) × 100

A yield of 3–5% is considered good. Some companies reinvest all profits and pay no dividend (growth companies like Zomato).

**Important dates:**
- **Record date** — you must own the stock on this date to receive the dividend
- **Ex-dividend date** — buy before this date to qualify
        """)

    with st.expander("What is SEBI?"):
        st.markdown("""
**SEBI = Securities and Exchange Board of India**

SEBI is the regulator of India's stock markets — like RBI is for banks.

**What SEBI does:**
- Protects investors from fraud
- Regulates stock exchanges, brokers, mutual funds
- Sets rules for IPOs and corporate disclosures
- Investigates insider trading

Think of SEBI as the referee in a cricket match — it makes sure everyone plays by the rules.
        """)

# ══════════════════════════════════════════════════════════════
with tab2:
    st.header("Charts & Candlesticks")

    with st.expander("What is a Candlestick chart?", expanded=True):
        st.markdown("""
A **candlestick** is the most popular way to visualise a stock's price movement for a given time period (1 minute, 1 day, 1 week, etc).

Each candle shows **4 prices**:
- **Open** — price at the start of the period
- **High** — highest price reached
- **Low** — lowest price reached
- **Close** — price at the end of the period

**Green candle** = Close > Open (price went UP)
**Red candle** = Close < Open (price went DOWN)
                     High
     |
_____|_____
|         |   ← Body (Open to Close)
|_________|
     |
    Low
                    The thin lines above and below the body are called **wicks** or **shadows**.

**Why it matters:**
A long upper wick means buyers pushed the price up but sellers brought it back down — bearish sign.
A long lower wick means sellers pushed it down but buyers brought it back — bullish sign.
        """)

    with st.expander("Key Candlestick Patterns"):
        st.markdown("""
**Bullish Patterns (suggest price may go up):**

🟢 **Hammer**
- Small body, long lower wick
- Appears after a downtrend
- Means sellers tried to push price down but buyers fought back strongly

🟢 **Bullish Engulfing**
- A large green candle completely covers the previous red candle
- Strong reversal signal

🟢 **Morning Star**
- Three candles: red, small (indecision), green
- Signals the end of a downtrend

---

**Bearish Patterns (suggest price may go down):**

🔴 **Shooting Star**
- Small body, long upper wick
- Appears after an uptrend
- Means buyers pushed price up but sellers overwhelmed them

🔴 **Bearish Engulfing**
- A large red candle completely covers the previous green candle
- Strong reversal signal

🔴 **Evening Star**
- Three candles: green, small, red
- Signals the end of an uptrend

---

**Neutral / Indecision:**

⚪ **Doji**
- Open and close are nearly equal — tiny body
- Neither buyers nor sellers in control
- Often signals a reversal when it appears after a strong trend
        """)

    with st.expander("Support and Resistance"):
        st.markdown("""
**Support** is a price level where a stock tends to stop falling and bounce back up.
**Resistance** is a price level where a stock tends to stop rising and fall back down.

Think of it like a floor and a ceiling.

**Why do they form?**
- Many traders have bought/sold at these levels before
- Psychological round numbers (e.g. ₹1000, ₹500) act as support/resistance
- Previous highs and lows become future reference points

**How to use:**
- If a stock is approaching support → possible buying opportunity
- If approaching resistance → consider taking profits
- When resistance is broken → it often becomes new support (called a breakout)

**Example:**
> HDFC Bank has held ₹1,600 as support three times in the last year. Each time it dropped to ₹1,600, buyers stepped in and pushed it back up. This makes ₹1,600 a strong support level.
        """)

    with st.expander("Trend Lines and Channels"):
        st.markdown("""
**Uptrend** — stock makes higher highs and higher lows. Draw a line connecting the lows.
**Downtrend** — stock makes lower highs and lower lows. Draw a line connecting the highs.
**Sideways** — stock moves within a range. Neither buyers nor sellers in control.

**Channel** — when you draw both a trendline and a parallel line above it, you get a channel. Price tends to bounce between the two lines.

**Breakout** — when price moves decisively outside a channel or breaks through resistance. Often followed by a big move in the breakout direction.

**The trend is your friend** — one of the oldest rules in trading. Always know what the overall trend is before entering a trade.
        """)

# ══════════════════════════════════════════════════════════════
with tab3:
    st.header("Technical Indicators")

    with st.expander("Moving Averages (MA)", expanded=True):
        st.markdown("""
A **Moving Average** smooths out price data to show the trend direction by averaging the closing prices over a set number of days.

**Simple Moving Average (SMA)**
= Average of closing prices over N days

**20-day MA** = average of last 20 days closing prices
**50-day MA** = average of last 50 days
**200-day MA** = long-term trend indicator

**How to read:**
- Price above MA → uptrend
- Price below MA → downtrend
- When a shorter MA crosses above a longer MA → **Golden Cross** (bullish)
- When a shorter MA crosses below a longer MA → **Death Cross** (bearish)

**Golden Cross Example:**
> The 50-day MA crosses above the 200-day MA for TCS.
> This has historically been a strong buy signal.
> The last time this happened in 2020, TCS went up 40% in the next 6 months.

**EMA (Exponential Moving Average)**
Similar to SMA but gives more weight to recent prices — reacts faster to price changes.
        """)

    with st.expander("RSI — Relative Strength Index"):
        st.markdown("""
**RSI** measures how fast and how much a stock's price has moved recently. It oscillates between 0 and 100.

**Formula (simplified):**
RSI = 100 - (100 / (1 + Average Gains / Average Losses))

**Reading RSI:**
| RSI Level | Meaning |
|-----------|---------|
| Above 70 | Overbought — stock may be due for a pullback |
| 30 to 70 | Neutral zone |
| Below 30 | Oversold — stock may be due for a recovery |

**How to use:**
- RSI below 30 + strong support nearby = potential buy
- RSI above 70 + near resistance = consider selling / avoid buying
- RSI divergence: price makes new high but RSI doesn't → weakness signal

**Important:** RSI alone is not enough. A stock can stay overbought for weeks during a strong uptrend. Always combine with other signals.

**Example:**
> SBI's RSI dropped to 25 in March 2020 (Covid crash). That was an extreme oversold signal. The stock doubled in the next 12 months.
        """)

    with st.expander("MACD — Moving Average Convergence Divergence"):
        st.markdown("""
**MACD** measures the relationship between two moving averages and shows momentum.

**Three components:**
1. **MACD Line** = 12-day EMA minus 26-day EMA
2. **Signal Line** = 9-day EMA of the MACD line
3. **Histogram** = MACD line minus Signal line (shown as bars)

**How to read:**
- MACD crosses **above** Signal line → **Bullish crossover** (buy signal)
- MACD crosses **below** Signal line → **Bearish crossover** (sell signal)
- Histogram above zero → momentum is positive
- Histogram below zero → momentum is negative

**MACD Divergence:**
- Price makes new high but MACD histogram gets smaller → trend weakening
- Price makes new low but MACD makes higher low → potential reversal

**Best used for:**
Trend-following trades. MACD works well in trending markets but gives false signals in sideways markets.
        """)

    with st.expander("Bollinger Bands"):
        st.markdown("""
**Bollinger Bands** consist of three lines:
- **Middle band** = 20-day Simple Moving Average
- **Upper band** = Middle band + 2 standard deviations
- **Lower band** = Middle band - 2 standard deviations

The bands expand when volatility is high and contract when volatility is low.

**How to read:**
- Price touching **upper band** → potentially overbought
- Price touching **lower band** → potentially oversold
- **Bollinger Squeeze** — when bands get very tight → big move coming (direction unknown)
- **Breakout** — price moving outside bands → continuation of strong trend

**The Bounce Strategy:**
Buy when price touches lower band in an uptrend and sell when it reaches upper band.

**Example:**
> Asian Paints was in a steady uptrend. Each time it touched the lower Bollinger Band, it bounced back up. A trader using this strategy would have caught multiple profitable trades.
        """)

    with st.expander("Volume"):
        st.markdown("""
**Volume** is the number of shares traded in a given period. It is the most honest indicator because it shows real money moving.

**Key rules:**

✅ **Price up + Volume up** = Strong move, likely to continue
⚠️ **Price up + Volume down** = Weak move, may not sustain
✅ **Price down + Volume up** = Strong selling, bearish
⚠️ **Price down + Volume down** = Weak selling, may reverse

**Volume Spikes:**
A sudden large spike in volume often signals a major event — earnings, news, institutional buying/selling.

**On-Balance Volume (OBV):**
Adds volume on up days, subtracts on down days. Rising OBV with rising price confirms uptrend. OBV rising while price is flat = accumulation (smart money buying quietly).
        """)

    with st.expander("Fibonacci Retracement"):
        st.markdown("""
**Fibonacci retracement** uses mathematical ratios to identify potential support and resistance levels.

The key levels are: **23.6%, 38.2%, 50%, 61.8%, 78.6%**

These come from the Fibonacci sequence (a mathematical pattern found throughout nature).

**How to use:**
1. Identify a significant swing high and swing low
2. Draw Fibonacci levels between them
3. These levels become potential support/resistance during retracements

**Most watched level: 61.8%** (the "golden ratio")

**Example:**
> Nifty 50 rallied from 16,000 to 20,000. During a correction, traders watch the 38.2% level (≈18,470) and 61.8% level (≈17,528) as potential buying zones.

**Why it works:** Enough traders watch these levels that they become self-fulfilling — when price reaches 61.8%, many traders place buy orders there, creating support.
        """)

# ══════════════════════════════════════════════════════════════
with tab4:
    st.header("Trading Styles")

    with st.expander("Intraday Trading (Day Trading)", expanded=True):
        st.markdown("""
**What it is:** Buying and selling stocks within the same trading day. All positions are closed before market close (3:30 PM IST).

**Time frame:** Minutes to hours

**Tools used:** 1-minute, 5-minute, 15-minute candlestick charts

**Pros:**
- No overnight risk
- Can profit in both rising and falling markets
- Capital is free every evening

**Cons:**
- Very stressful and time-intensive
- Requires full attention during market hours
- High brokerage costs from frequent trades
- 90%+ of intraday traders lose money

**Who it suits:** Full-time traders with strong discipline, fast execution, and ability to handle losses calmly.

**Margin:** Brokers offer up to 5x leverage for intraday — you can trade ₹5,00,000 with just ₹1,00,000. This amplifies both gains AND losses.

⚠️ **Not recommended for beginners.**
        """)

    with st.expander("Swing Trading"):
        st.markdown("""
**What it is:** Holding stocks for a few days to a few weeks to capture a price "swing."

**Time frame:** 2 days to 6 weeks

**Tools used:** Daily and weekly candlestick charts, RSI, MACD, support/resistance

**Strategy:**
1. Identify a stock in a clear trend
2. Wait for a pullback to support
3. Enter when price shows reversal signals
4. Set a target at the next resistance level
5. Set a stop loss below the recent low

**Pros:**
- Less stressful than intraday
- Can be done part-time
- Better risk/reward ratios possible

**Cons:**
- Overnight and weekend risk
- Requires patience

**Example:**
> Infosys is in an uptrend. It pulls back to its 50-day MA. RSI drops to 42 (not oversold but cooling off). MACD histogram shrinks. A swing trader enters here targeting the previous high. Stop loss just below the 50-day MA.

**Best for:** Working professionals who can check charts in the evening.
        """)

    with st.expander("Positional Trading"):
        st.markdown("""
**What it is:** Holding stocks for weeks to months based on fundamental + technical analysis.

**Time frame:** 1 month to 1 year

**Tools used:** Weekly charts, moving averages, sector trends, company fundamentals

**Approach:**
- Identify sectors doing well (e.g. infrastructure boom)
- Find best stocks in that sector
- Enter during corrections
- Hold until the trend changes

**Pros:**
- Lower transaction costs
- Less time monitoring
- Can compound returns significantly

**Cons:**
- Capital locked up for months
- Requires conviction during drawdowns

**Example:**
> In early 2023, a positional trader identified the defence sector as a multi-year theme. HAL and BEL were entered on pullbacks. By end of 2024, both had given 2-3x returns.
        """)

    with st.expander("Long-term Investing"):
        st.markdown("""
**What it is:** Buying quality companies and holding for years or decades. The Warren Buffett approach.

**Time frame:** 3 years to forever

**Approach:**
- Focus on business quality, not short-term price
- Look at earnings growth, debt levels, return on equity
- Buy during market crashes when good stocks are cheap
- Ignore daily price fluctuations

**Key metrics to check:**
| Metric | What it tells you |
|--------|------------------|
| P/E Ratio | How expensive the stock is vs earnings |
| P/B Ratio | Price vs book value of company assets |
| ROE | How efficiently the company uses shareholder money |
| Debt/Equity | How much debt the company carries |
| EPS Growth | Whether earnings are growing year on year |

**The power of compounding:**
₹1,00,000 invested in Infosys in 2003 would be worth over ₹2 crore today (20x in 20 years).

**Best for:** Everyone. Even active traders should have a long-term portfolio running alongside.
        """)

    with st.expander("Options Trading"):
        st.markdown("""
**What it is:** Trading contracts that give you the right (but not obligation) to buy or sell a stock at a specific price before a specific date.

**Two types:**
- **Call option** — right to BUY at a fixed price (profit when stock goes up)
- **Put option** — right to SELL at a fixed price (profit when stock goes down)

**Key terms:**
- **Strike price** — the fixed price in the contract
- **Premium** — what you pay to buy the option
- **Expiry** — the date the contract expires (every Thursday in India for weekly options)

**Why options:**
- Can profit with a small amount of capital
- Can hedge your existing stock positions
- Can profit in any market direction

**Example:**
> Nifty is at 22,000. You buy a Call option with strike 22,200 for ₹150 premium.
> If Nifty goes to 22,500, your option is now worth ₹300 — you doubled your money.
> If Nifty stays below 22,200, your ₹150 is lost.

⚠️ **Options are complex and highly risky. 95% of option buyers lose money. Learn thoroughly before trading options.**
        """)

# ══════════════════════════════════════════════════════════════
with tab5:
    st.header("Risk Management")

    with st.expander("The most important skill in trading", expanded=True):
        st.markdown("""
**Risk management is more important than picking the right stock.**

Even the best traders are wrong 40–50% of the time. What separates profitable traders from losing ones is how much they lose when wrong vs how much they gain when right.

**The golden rule:** Never risk more than 1–2% of your total capital on a single trade.

If you have ₹1,00,000:
- Maximum loss per trade = ₹1,000 to ₹2,000
- This means even 10 losses in a row only loses you 10–20%
- You stay in the game long enough to let your edge work

**Why most traders blow up their account:**
They risk too much per trade. After 3–4 losses in a row (which happens to everyone), they've lost 40–60% of their capital. Psychologically impossible to recover from.
        """)

    with st.expander("Stop Loss — your best friend"):
        st.markdown("""
A **stop loss** is a pre-set price at which you automatically exit a trade to limit your loss.

**Example:**
> You buy Axis Bank at ₹1,200. You set a stop loss at ₹1,150.
> If it falls to ₹1,150, your position is automatically sold.
> Maximum loss = ₹50 per share.

**Where to place stop loss:**
- Below the recent swing low (for long trades)
- Below the support level
- Below the 50-day MA for medium-term trades
- 1–2% below entry for tight intraday trades

**Never move your stop loss down** — this is how small losses become catastrophic losses.

**Trailing stop loss:** Moves up as the stock goes up, locking in profits while still giving room to run.
        """)

    with st.expander("Position Sizing"):
        st.markdown("""
**Position sizing** = how many shares to buy in each trade

**Formula:**
Number of Shares = (Capital at Risk) / (Entry Price - Stop Loss Price)

**Example:**
> You have ₹1,00,000. You're willing to risk 1% = ₹1,000.
> You want to buy Wipro at ₹450 with a stop loss at ₹430.
> Risk per share = ₹450 - ₹430 = ₹20
> Number of shares = ₹1,000 / ₹20 = **50 shares**
> Total position size = 50 × ₹450 = ₹22,500

This keeps your risk fixed at ₹1,000 regardless of the stock price.

**Why this matters:**
Without position sizing, traders often buy "round lots" (100 shares, 500 shares) with no logical basis. This leads to over-exposure on some trades and under-exposure on others.
        """)

    with st.expander("Risk/Reward Ratio"):
        st.markdown("""
**Risk/Reward Ratio** = Potential Loss : Potential Gain

**Aim for at least 1:2** — risk ₹1 to make ₹2.

**Example:**
> Entry: ₹500
> Stop loss: ₹480 (risk = ₹20)
> Target: ₹540 (reward = ₹40)
> Risk/Reward = 1:2 ✅

**Why it matters:**
Even if you are right only 40% of the time, a 1:2 R:R makes you profitable:
- 4 winning trades × ₹40 = ₹160
- 6 losing trades × ₹20 = ₹120 loss
- Net profit = ₹40

**Never take trades with R:R below 1:1.5.** The math won't work in your favour long term.
        """)

    with st.expander("Common Mistakes to Avoid"):
        st.markdown("""
**1. Averaging down on losing trades**
> Buying more of a stock that is falling to "reduce the average cost." This turns small losses into devastating ones if the stock keeps falling.

**2. Not using a stop loss**
> "It will come back." Sometimes it doesn't. Satyam, Yes Bank, DHFL — investors who held without stops lost everything.

**3. Overtrading**
> Taking too many trades out of boredom or FOMO. Each trade has a cost (brokerage, taxes). Quality over quantity.

**4. Revenge trading**
> After a loss, immediately taking another trade to "make it back." Emotional trading leads to bigger losses.

**5. Ignoring taxes**
> In India: Short-term capital gains (STCG) on stocks held < 1 year = 20%. Long-term capital gains (LTCG) > 1 year = 12.5% above ₹1.25 lakh. Factor taxes into your profit calculations.

**6. FOMO buying**
> Buying a stock after it has already run up 30% because you don't want to miss out. You're buying someone else's profit.
        """)

# ══════════════════════════════════════════════════════════════
with tab6:
    st.header("Indian Stock Market")

    with st.expander("Market Hours and Sessions", expanded=True):
        st.markdown("""
**Indian stock markets are open Monday to Friday** (closed on public holidays).

| Session | Time (IST) | Description |
|---------|-----------|-------------|
| Pre-market | 9:00 AM – 9:15 AM | Order collection, price discovery |
| Normal market | 9:15 AM – 3:30 PM | Regular trading |
| Post-market | 3:40 PM – 4:00 PM | Closing price session |

**Most volatile periods:**
- First 30 minutes (9:15–9:45 AM) — high volume, big moves
- Last 30 minutes (3:00–3:30 PM) — institutional activity before close

**F&O Expiry:** Every Thursday (weekly) and last Thursday of the month (monthly). Volatility increases on expiry days.
        """)

    with st.expander("Key Indian Indices"):
        st.markdown("""
| Index | Exchange | Composition | What it represents |
|-------|----------|-------------|-------------------|
| Nifty 50 | NSE | Top 50 stocks | Large-cap India |
| Sensex | BSE | Top 30 stocks | Blue-chip India |
| Nifty Bank | NSE | Top 12 banking stocks | Banking sector |
| Nifty IT | NSE | Top IT companies | Technology sector |
| Nifty Midcap 100 | NSE | Top 100 mid-cap | Mid-size companies |
| Nifty Smallcap 100 | NSE | Top 100 small-cap | Small companies |

**Sector indices** allow you to track specific industries — pharma, FMCG, auto, infra, etc.
        """)

    with st.expander("How to Start Investing in India"):
        st.markdown("""
**Step 1: Open a Demat + Trading Account**
You need a Demat account (holds your shares electronically) and a Trading account (to buy/sell).

**Popular brokers:**
- **Zerodha** — low cost, good platform (Kite)
- **Groww** — beginner-friendly
- **Angel One** — good research tools
- **Upstox** — competitive pricing

**Documents needed:** PAN card, Aadhaar, bank account, signature

**Step 2: Complete KYC**
Your broker will verify your identity online (e-KYC via Aadhaar OTP).

**Step 3: Add Funds**
Transfer money from your bank to your trading account.

**Step 4: Start with Large Caps**
Begin with well-known, stable companies. Avoid penny stocks and highly volatile small caps initially.
        """)

    with st.expander("Taxes on Stock Market in India"):
        st.markdown("""
**Capital Gains Tax (as of 2024–25 budget):**

| Type | Holding Period | Tax Rate |
|------|---------------|---------|
| Short-Term Capital Gains (STCG) | Less than 1 year | 20% |
| Long-Term Capital Gains (LTCG) | More than 1 year | 12.5% (above ₹1.25 lakh) |

**F&O Trading Tax:**
Options and futures profits are taxed as **business income** at your applicable income tax slab rate. Losses can be carried forward for 8 years.

**Securities Transaction Tax (STT):**
Automatically deducted on every trade. For equity delivery: 0.1% on buy and sell. For intraday and F&O: different rates.

**Tip:** Maintain a trade book and use a CA or tax software (like Quicko or ClearTax) to file ITR-2 or ITR-3 accurately.
        """)

    with st.expander("Useful SEBI Rules for Retail Investors"):
        st.markdown("""
**T+1 Settlement:**
Since 2023, India moved to T+1 settlement — shares bought today appear in your Demat by the next trading day.

**Circuit Breakers:**
If a stock rises or falls more than a set limit (5%, 10%, 20%), trading is paused. This prevents panic crashes.

**SEBI Investor Protection Fund:**
If a broker defaults, SEBI's fund can compensate investors up to ₹25 lakh.

**Nomination:**
Always add a nominee to your Demat account. If something happens to you, your holdings can be transferred to your nominee.

**SCORES Portal:**
If you have a complaint against a broker or listed company, file it at scores.sebi.gov.in — SEBI's official complaint portal.
        """)