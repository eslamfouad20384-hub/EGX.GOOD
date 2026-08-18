import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import ta

from concurrent.futures import ThreadPoolExecutor, as_completed


# =========================================================
# 🚀 EGX AI PRO MAX V6
# PRODUCTION / LIQUIDITY / RS / SECTOR / BACKTEST
# =========================================================

st.set_page_config(
    page_title="EGX AI PRO MAX V6",
    page_icon="📈",
    layout="wide"
)

st.title("🚀 EGX AI PRO MAX V6")
st.caption(
    "EGX Scanner • Multi-Timeframe • Liquidity • Relative Strength • "
    "Sector Ranking • Risk/Reward • Backtest"
)


# =========================================================
# 📌 UNIVERSE
# =========================================================

EGX100 = [
    "COMI.CA", "MFPC.CA", "PHDC.CA", "ACRI.CA", "ORAS.CA",
    "HRHO.CA", "TMGH.CA", "FWRY.CA", "SWDY.CA", "ETEL.CA",
    "AMOC.CA", "HELI.CA", "EAST.CA", "EFID.CA", "JUFO.CA",
    "ABUK.CA", "ESRS.CA", "EMFD.CA", "MNHD.CA", "CCAP.CA",
    "CICH.CA", "OCDI.CA", "ORHD.CA", "MASR.CA", "TAQA.CA",
    "ADIB.CA", "SAUD.CA", "QNBA.CA", "CIEB.CA", "FAIT.CA",
    "CANAL.CA", "EXPA.CA", "ARCC.CA", "AJWA.CA", "MICH.CA",
    "SUGR.CA", "POUL.CA", "DOMT.CA", "ISMA.CA", "UEGC.CA",
    "AUTO.CA", "OLFI.CA", "SKPC.CA", "AMER.CA", "TALM.CA",
    "ORWE.CA", "SPMD.CA", "ZMID.CA", "MENA.CA", "DAPH.CA",
    "RAYA.CA", "VERT.CA", "EGAL.CA", "ECAP.CA", "MPRC.CA",
    "NCCW.CA", "SCEM.CA", "ARAB.CA", "GDWA.CA", "ELEC.CA",
    "IRON.CA", "ATQA.CA", "EGCH.CA", "KIMA.CA", "ALCN.CA",
    "MPCO.CA", "ELSH.CA", "MEPA.CA", "ODIN.CA",
    "EGAS.CA", "RACC.CA", "PRCL.CA", "BINV.CA",
    "EDBM.CA", "MCQE.CA", "MOIL.CA", "NIPH.CA", "ISPH.CA",
    "DICE.CA", "IDHC.CA", "UNIT.CA", "PHAR.CA",
    "TRTO.CA", "ALRA.CA", "FARE.CA", "ICFC.CA", "MISr.CA",
    "MOBI.CA", "ELKA.CA", "NILE.CA", "ATLC.CA",
    "COSG.CA", "MEDA.CA", "AMPI.CA", "COPR.CA"
]

EGX100 = list(dict.fromkeys(EGX100))


# =========================================================
# 🏭 SECTORS
# =========================================================

SECTORS = {

    # Banks
    "COMI.CA": "Banks",
    "HRHO.CA": "Financial Services",
    "ADIB.CA": "Banks",
    "SAUD.CA": "Banks",
    "QNBA.CA": "Banks",
    "CIEB.CA": "Banks",
    "FAIT.CA": "Banks",
    "CANAL.CA": "Banks",
    "EXPA.CA": "Banks",
    "ARCC.CA": "Financial Services",
    "CICH.CA": "Financial Services",
    "BINV.CA": "Financial Services",
    "EDBM.CA": "Banks",

    # Real Estate
    "PHDC.CA": "Real Estate",
    "TMGH.CA": "Real Estate",
    "MNHD.CA": "Real Estate",
    "EMFD.CA": "Real Estate",
    "OCDI.CA": "Real Estate",
    "ORHD.CA": "Real Estate",
    "MASR.CA": "Real Estate",
    "AMER.CA": "Real Estate",
    "TALM.CA": "Real Estate",
    "MENA.CA": "Real Estate",
    "ODIN.CA": "Real Estate",
    "RACC.CA": "Real Estate",

    # Petrochemicals / Chemicals
    "MFPC.CA": "Chemicals",
    "AMOC.CA": "Petrochemicals",
    "SKPC.CA": "Petrochemicals",
    "ABUK.CA": "Chemicals",
    "EGAS.CA": "Energy",
    "TAQA.CA": "Energy",
    "EGCH.CA": "Chemicals",
    "KIMA.CA": "Chemicals",
    "ECAP.CA": "Chemicals",
    "MICH.CA": "Chemicals",

    # Industrial
    "SWDY.CA": "Industrials",
    "ESRS.CA": "Steel",
    "IRON.CA": "Steel",
    "ORAS.CA": "Industrials",
    "ALCN.CA": "Industrials",
    "NCCW.CA": "Industrials",
    "SCEM.CA": "Industrials",
    "ATQA.CA": "Industrials",
    "MPCO.CA": "Industrials",
    "ELSH.CA": "Industrials",

    # Telecom / Technology
    "ETEL.CA": "Telecom",
    "FWRY.CA": "Technology",
    "RAYA.CA": "Technology",
    "MOBI.CA": "Technology",
    "IDHC.CA": "Healthcare Technology",

    # Food
    "EAST.CA": "Food & Tobacco",
    "EFID.CA": "Food",
    "JUFO.CA": "Food",
    "DOMT.CA": "Food",
    "POUL.CA": "Food",
    "OLFI.CA": "Food",
    "SUGR.CA": "Food",
    "ISMA.CA": "Food",
    "DICE.CA": "Consumer",

    # Healthcare
    "PHAR.CA": "Healthcare",
    "ISPH.CA": "Healthcare",
    "NIPH.CA": "Healthcare",
    "MEPA.CA": "Healthcare",

    # Other / Consumer
    "HELI.CA": "Real Estate",
    "ORWE.CA": "Consumer",
    "AUTO.CA": "Automotive",
    "MENA.CA": "Real Estate",
    "VERT.CA": "Financial Services",
    "DAPH.CA": "Consumer",
    "PRCL.CA": "Financial Services",
    "UNIT.CA": "Financial Services",
    "TRTO.CA": "Consumer",
    "ALRA.CA": "Consumer",
    "FARE.CA": "Financial Services",
    "ICFC.CA": "Financial Services",
    "COSG.CA": "Consumer",
    "MEDA.CA": "Consumer",
    "AMPI.CA": "Industrials",
    "COPR.CA": "Industrials",
}


# =========================================================
# 🎛️ SETTINGS
# =========================================================

st.sidebar.header("⚙️ إعدادات الفحص")

period_daily = st.sidebar.selectbox(
    "الفترة اليومية",
    ["1y", "2y", "3y", "5y"],
    index=2
)

period_weekly = st.sidebar.selectbox(
    "الفترة الأسبوعية",
    ["2y", "3y", "5y", "10y"],
    index=1
)

period_monthly = st.sidebar.selectbox(
    "الفترة الشهرية",
    ["3y", "5y", "10y", "max"],
    index=1
)

max_workers = st.sidebar.slider(
    "⚡ الاتصالات المتوازية",
    2,
    16,
    8
)

top_n = st.sidebar.slider(
    "🏆 أفضل عدد أسهم",
    5,
    50,
    20,
    5
)

min_liquidity = st.sidebar.number_input(
    "💧 الحد الأدنى لمتوسط قيمة التداول اليومية EGP",
    min_value=0.0,
    value=5_000_000.0,
    step=500_000.0
)

backtest_horizon = st.sidebar.slider(
    "🧪 Backtest Horizon",
    5,
    60,
    20
)

min_score = st.sidebar.slider(
    "🎯 أقل Score للفرص القوية",
    50,
    90,
    70
)

st.sidebar.markdown("---")

st.sidebar.metric(
    "📊 الكون المطلوب",
    len(EGX100)
)


# =========================================================
# 📥 DATA DOWNLOAD
# =========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def load_data(symbols, period, interval):

    if not symbols:
        return pd.DataFrame()

    try:

        return yf.download(
            tickers=symbols,
            period=period,
            interval=interval,
            group_by="ticker",
            threads=True,
            auto_adjust=True,
            progress=False
        )

    except Exception:
        return pd.DataFrame()


# =========================================================
# 📊 SINGLE SYMBOL EXTRACTION
# =========================================================

def extract_symbol_data(data, symbol):

    try:

        if data is None or data.empty:
            return pd.DataFrame()

        if isinstance(data.columns, pd.MultiIndex):

            levels = data.columns.get_level_values

            if symbol in levels(0):
                df = data[symbol].copy()

            elif symbol in levels(1):
                df = data.xs(
                    symbol,
                    axis=1,
                    level=1
                ).copy()

            else:
                return pd.DataFrame()

        else:

            df = data.copy()

        required = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        if not all(
            c in df.columns
            for c in required
        ):
            return pd.DataFrame()

        df = df[required].copy()

        df = df.replace(
            [np.inf, -np.inf],
            np.nan
        )

        df = df.dropna(
            subset=["Close"]
        )

        df = df.sort_index()

        return df

    except Exception:
        return pd.DataFrame()


# =========================================================
# 📈 INDICATORS
# =========================================================

def add_indicators(df):

    df = df.copy()

    if len(df) < 50:
        return df

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    # -------------------------
    # EMA
    # -------------------------

    df["ema20"] = close.ewm(
        span=20,
        adjust=False
    ).mean()

    df["ema50"] = close.ewm(
        span=50,
        adjust=False
    ).mean()

    df["ema200"] = close.ewm(
        span=200,
        adjust=False
    ).mean()

    # -------------------------
    # RSI
    # -------------------------

    df["rsi"] = ta.momentum.RSIIndicator(
        close,
        window=14
    ).rsi()

    # -------------------------
    # MACD
    # -------------------------

    macd = ta.trend.MACD(
        close,
        window_slow=26,
        window_fast=12,
        window_sign=9
    )

    df["macd"] = macd.macd()

    df["macd_signal"] = (
        macd.macd_signal()
    )

    df["macd_hist"] = (
        macd.macd_diff()
    )

    # -------------------------
    # ATR
    # -------------------------

    df["atr"] = ta.volatility.AverageTrueRange(
        high,
        low,
        close,
        window=14
    ).average_true_range()

    # -------------------------
    # ADX
    # -------------------------

    df["adx"] = ta.trend.ADXIndicator(
        high,
        low,
        close,
        window=14
    ).adx()

    # -------------------------
    # Volume
    # -------------------------

    df["vol_ma20"] = (
        volume.rolling(20).mean()
    )

    df["volume_ratio"] = (
        volume /
        (df["vol_ma20"] + 1e-9)
    )

    # -------------------------
    # Traded Value
    # -------------------------

    df["traded_value"] = (
        close * volume
    )

    df["avg_traded_value"] = (
        df["traded_value"]
        .rolling(20)
        .mean()
    )

    # -------------------------
    # OBV
    # -------------------------

    try:

        df["obv"] = (
            ta.volume
            .OnBalanceVolumeIndicator(
                close,
                volume
            )
            .on_balance_volume()
        )

        df["obv_ma20"] = (
            df["obv"]
            .rolling(20)
            .mean()
        )

    except Exception:

        df["obv"] = np.nan
        df["obv_ma20"] = np.nan

    # -------------------------
    # Money Flow
    # -------------------------

    try:

        df["mfi"] = (
            ta.volume
            .MoneyFlowIndex(
                high,
                low,
                close,
                volume,
                window=14
            )
        )

    except Exception:

        df["mfi"] = np.nan

    # -------------------------
    # Support / Resistance
    # -------------------------

    df["support20"] = (
        low.rolling(20).min()
    )

    df["resistance20"] = (
        high.rolling(20).max()
    )

    df["support60"] = (
        low.rolling(60).min()
    )

    df["resistance60"] = (
        high.rolling(60).max()
    )

    # -------------------------
    # Returns
    # -------------------------

    df["return_20"] = (
        close.pct_change(20)
    )

    df["return_60"] = (
        close.pct_change(60)
    )

    return df


# =========================================================
# 💧 LIQUIDITY SCORE
# =========================================================

def liquidity_score(last):

    avg_value = float(
        last.get(
            "avg_traded_value",
            0
        )
    )

    volume_ratio = float(
        last.get(
            "volume_ratio",
            0
        )
    )

    score = 0

    if avg_value >= 100_000_000:
        score += 70

    elif avg_value >= 50_000_000:
        score += 60

    elif avg_value >= 20_000_000:
        score += 50

    elif avg_value >= 10_000_000:
        score += 40

    elif avg_value >= 5_000_000:
        score += 30

    elif avg_value >= 1_000_000:
        score += 15

    if volume_ratio >= 2:
        score += 20

    elif volume_ratio >= 1.5:
        score += 15

    elif volume_ratio >= 1:
        score += 10

    return min(
        100,
        score
    )


# =========================================================
# 📈 RELATIVE STRENGTH
# =========================================================

def calculate_relative_strength(
    stock_df,
    benchmark_df
):

    try:

        if stock_df.empty:
            return 50, 0

        if benchmark_df.empty:
            return 50, 0

        s = stock_df["Close"].copy()
        b = benchmark_df["Close"].copy()

        combined = pd.concat(
            [s, b],
            axis=1,
            join="inner"
        )

        combined.columns = [
            "stock",
            "benchmark"
        ]

        combined = combined.dropna()

        if len(combined) < 30:
            return 50, 0

        stock_return = (
            combined["stock"].iloc[-1] /
            combined["stock"].iloc[-21] -
            1
        )

        bench_return = (
            combined["benchmark"].iloc[-1] /
            combined["benchmark"].iloc[-21] -
            1
        )

        rs = (
            stock_return -
            bench_return
        )

        score = 50 + (
            rs * 250
        )

        score = max(
            0,
            min(100, score)
        )

        return score, rs * 100

    except Exception:
        return 50, 0


# =========================================================
# 🏭 SECTOR SCORE
# =========================================================

def calculate_sector_scores(
    data_dict
):

    sector_returns = {}

    for symbol, df in data_dict.items():

        try:

            if df.empty:
                continue

            sector = SECTORS.get(
                symbol,
                "Other"
            )

            if len(df) < 21:
                continue

            ret = (
                df["Close"].iloc[-1] /
                df["Close"].iloc[-21] -
                1
            )

            sector_returns.setdefault(
                sector,
                []
            )

            sector_returns[
                sector
            ].append(ret)

        except Exception:
            continue

    sector_scores = {}

    for sector, values in sector_returns.items():

        if not values:
            continue

        avg_return = np.mean(
            values
        )

        score = 50 + (
            avg_return * 250
        )

        sector_scores[sector] = max(
            0,
            min(100, score)
        )

    return sector_scores


# =========================================================
# 🧠 MARKET REGIME
# =========================================================

def market_regime(last):

    score = 0

    if last["Close"] > last["ema200"]:
        score += 1

    if last["ema20"] > last["ema50"]:
        score += 1

    if last["macd"] > 0:
        score += 1

    if last["rsi"] > 50:
        score += 1

    if last["adx"] > 20:
        score += 1

    if score >= 5:
        return "🚀 قوي جداً"

    if score == 4:
        return "🟢 صعود قوي"

    if score == 3:
        return "🟢 صعود"

    if score == 2:
        return "⚠️ محايد"

    return "🔴 هبوط"


# =========================================================
# 🧠 TECHNICAL SCORE
# =========================================================

def technical_score(
    d,
    w,
    m
):

    score = 0

    # -------------------------
    # Trend = 35
    # -------------------------

    if d["Close"] > d["ema200"]:
        score += 10

    if d["ema20"] > d["ema50"]:
        score += 5

    if w["Close"] > w["ema200"]:
        score += 8

    if m["Close"] > m["ema200"]:
        score += 7

    if d["ema50"] > d["ema200"]:
        score += 5

    # -------------------------
    # Momentum = 25
    # -------------------------

    if 50 <= d["rsi"] <= 68:
        score += 8

    elif 45 <= d["rsi"] < 50:
        score += 4

    if d["macd"] > d["macd_signal"]:
        score += 6

    if d["macd_hist"] > 0:
        score += 4

    if d["adx"] >= 25:
        score += 7

    elif d["adx"] >= 20:
        score += 4

    # -------------------------
    # Volume = 15
    # -------------------------

    if d["volume_ratio"] >= 2:
        score += 8

    elif d["volume_ratio"] >= 1.5:
        score += 6

    elif d["volume_ratio"] >= 1:
        score += 3

    if (
        pd.notna(d["obv"]) and
        pd.notna(d["obv_ma20"]) and
        d["obv"] > d["obv_ma20"]
    ):
        score += 4

    if pd.notna(d["mfi"]):

        if 50 <= d["mfi"] <= 80:
            score += 3

    # -------------------------
    # Volatility / stability
    # -------------------------

    atr_pct = (
        d["atr"] /
        d["Close"] *
        100
    )

    if 1.5 <= atr_pct <= 5:
        score += 5

    elif atr_pct <= 7:
        score += 2

    return min(
        100,
        score
    )


# =========================================================
# 🎯 TRADE PLAN
# =========================================================

def trade_plan(
    df,
    technical
):

    last = df.iloc[-1]

    entry = float(
        last["Close"]
    )

    atr_value = float(
        last["atr"]
    )

    support = float(
        last["support20"]
    )

    resistance = float(
        last["resistance20"]
    )

    if entry <= 0 or atr_value <= 0:
        raise ValueError(
            "Invalid trade values"
        )

    bullish = (
        last["ema20"] >
        last["ema50"] and
        last["Close"] >
        last["ema200"]
    )

    # -------------------------
    # STOP
    # -------------------------

    atr_stop = (
        entry -
        atr_value * 1.5
    )

    support_stop = (
        support -
        atr_value * 0.25
    )

    stop = max(
        atr_stop,
        support_stop
    )

    if stop >= entry:
        stop = (
            entry -
            atr_value * 1.5
        )

    risk = entry - stop

    # -------------------------
    # TP1
    # -------------------------

    tp1_r = entry + risk * 1.0

    # nearest resistance if above entry
    if resistance > entry:

        tp1 = min(
            resistance,
            tp1_r
        )

        if tp1 <= entry:
            tp1 = tp1_r

    else:
        tp1 = tp1_r

    # -------------------------
    # TP2
    # -------------------------

    tp2 = entry + risk * 2.0

    if resistance > tp1:

        tp2 = max(
            tp2,
            resistance
        )

    # -------------------------
    # TP3
    # -------------------------

    tp3 = entry + risk * 3.0

    resistance60 = float(
        last.get(
            "resistance60",
            tp3
        )
    )

    if resistance60 > tp2:

        tp3 = max(
            tp3,
            resistance60
        )

    # -------------------------
    # R/R
    # -------------------------

    rr1 = (
        (tp1 - entry) /
        risk
        if risk > 0
        else 0
    )

    rr2 = (
        (tp2 - entry) /
        risk
        if risk > 0
        else 0
    )

    rr3 = (
        (tp3 - entry) /
        risk
        if risk > 0
        else 0
    )

    return {
        "Entry": entry,
        "SL": stop,
        "TP1": tp1,
        "TP2": tp2,
        "TP3": tp3,
        "RR_TP1": rr1,
        "RR_TP2": rr2,
        "RR_TP3": rr3,
        "Bullish": bullish
    }


# =========================================================
# 🧪 BACKTEST
# =========================================================

def backtest_stock(
    df,
    horizon=20
):

    try:

        if len(df) < 260:
            return {
                "BT_Trades": 0,
                "BT_WinRate": 0,
                "BT_TP1Rate": 0,
                "BT_AvgReturn": 0,
                "BT_Confidence": 0
            }

        data = add_indicators(
            df.copy()
        )

        data = data.dropna(
            subset=[
                "ema50",
                "ema200",
                "rsi",
                "macd",
                "atr",
                "adx"
            ]
        )

        if len(data) < 200:
            return {
                "BT_Trades": 0,
                "BT_WinRate": 0,
                "BT_TP1Rate": 0,
                "BT_AvgReturn": 0,
                "BT_Confidence": 0
            }

        trades = []

        # sample every 5 sessions
        # to reduce overfitting and processing time
        indices = range(
            200,
            len(data) - horizon,
            5
        )

        for i in indices:

            row = data.iloc[i]

            # historical signal
            trend = (
                row["Close"] >
                row["ema200"]
            )

            momentum = (
                row["ema20"] >
                row["ema50"] and
                row["macd"] >
                row["macd_signal"]
            )

            rsi_ok = (
                45 <
                row["rsi"] <
                70
            )

            adx_ok = (
                row["adx"] >= 20
            )

            if not (
                trend and
                momentum and
                rsi_ok and
                adx_ok
            ):
                continue

            entry = float(
                row["Close"]
            )

            atr_value = float(
                row["atr"]
            )

            if (
                not np.isfinite(entry) or
                not np.isfinite(atr_value) or
                atr_value <= 0
            ):
                continue

            sl = (
                entry -
                atr_value * 1.5
            )

            tp1 = (
                entry +
                atr_value * 1.5
            )

            future = data.iloc[
                i + 1:
                i + 1 + horizon
            ]

            hit_tp = False
            hit_sl = False

            for _, candle in future.iterrows():

                high = float(
                    candle["High"]
                )

                low = float(
                    candle["Low"]
                )

                # conservative:
                # if both occur same candle,
                # SL is assumed first
                if (
                    low <= sl and
                    high >= tp1
                ):
                    hit_sl = True
                    break

                if low <= sl:

                    hit_sl = True
                    break

                if high >= tp1:

                    hit_tp = True
                    break

            if hit_tp:

                trades.append(
                    {
                        "win": 1,
                        "return": (
                            tp1 / entry - 1
                        )
                    }
                )

            elif hit_sl:

                trades.append(
                    {
                        "win": 0,
                        "return": (
                            sl / entry - 1
                        )
                    }
                )

        if not trades:

            return {
                "BT_Trades": 0,
                "BT_WinRate": 0,
                "BT_TP1Rate": 0,
                "BT_AvgReturn": 0,
                "BT_Confidence": 0
            }

        wins = [
            x["win"]
            for x in trades
        ]

        returns = [
            x["return"]
            for x in trades
        ]

        trades_count = len(
            trades
        )

        win_rate = (
            np.mean(wins) * 100
        )

        avg_return = (
            np.mean(returns) * 100
        )

        # Confidence:
        # combines win rate + sample size
        sample_factor = min(
            1.0,
            trades_count / 30
        )

        confidence = (
            win_rate *
            sample_factor
        )

        return {
            "BT_Trades": trades_count,
            "BT_WinRate": win_rate,
            "BT_TP1Rate": win_rate,
            "BT_AvgReturn": avg_return,
            "BT_Confidence": confidence
        }

    except Exception:

        return {
            "BT_Trades": 0,
            "BT_WinRate": 0,
            "BT_TP1Rate": 0,
            "BT_AvgReturn": 0,
            "BT_Confidence": 0
        }


# =========================================================
# 🧠 FINAL SCORE
# =========================================================

def final_score(
    technical,
    liquidity,
    relative_strength,
    sector_score,
    rr_score,
    backtest_confidence
):

    score = (

        technical * 0.35 +

        liquidity * 0.15 +

        relative_strength * 0.15 +

        sector_score * 0.10 +

        rr_score * 0.10 +

        backtest_confidence * 0.15

    )

    return round(
        min(100, max(0, score)),
        2
    )


# =========================================================
# 🎯 SIGNAL
# =========================================================

def signal_from_score(score):

    if score >= 85:
        return "🔥 STRONG BUY"

    if score >= 75:
        return "🟢 BUY"

    if score >= 65:
        return "🟡 WATCH"

    if score >= 50:
        return "⚠️ NEUTRAL"

    return "🔴 WEAK"


# =========================================================
# ⏱️ TIME ESTIMATION
# =========================================================

def time_estimation(
    atr_pct
):

    if atr_pct >= 5:
        return "1 - 3 weeks"

    if atr_pct >= 3:
        return "3 - 8 weeks"

    if atr_pct >= 1.5:
        return "1 - 3 months"

    return "3 - 6 months"


# =========================================================
# ⚙️ PROCESS STOCK
# =========================================================

def process_stock(
    symbol,
    daily,
    weekly,
    monthly,
    benchmark,
    sector_scores,
    min_liquidity,
    backtest_horizon
):

    clean_symbol = symbol.replace(
        ".CA",
        ""
    )

    try:

        df_d = extract_symbol_data(
            daily,
            symbol
        )

        df_w = extract_symbol_data(
            weekly,
            symbol
        )

        df_m = extract_symbol_data(
            monthly,
            symbol
        )

        if df_d.empty:
            return {
                "Symbol": clean_symbol,
                "Status": "❌ Daily"
            }

        if df_w.empty:
            return {
                "Symbol": clean_symbol,
                "Status": "❌ Weekly"
            }

        if df_m.empty:
            return {
                "Symbol": clean_symbol,
                "Status": "❌ Monthly"
            }

        # -------------------------
        # indicators
        # -------------------------

        df_d = add_indicators(
            df_d
        )

        df_w = add_indicators(
            df_w
        )

        df_m = add_indicators(
            df_m
        )

        required_d = [
            "ema20",
            "ema50",
            "ema200",
            "rsi",
            "macd",
            "macd_signal",
            "macd_hist",
            "atr",
            "adx",
            "vol_ma20",
            "volume_ratio",
            "avg_traded_value",
            "support20",
            "resistance20"
        ]

        if not all(
            c in df_d.columns
            for c in required_d
        ):
            return {
                "Symbol": clean_symbol,
                "Status": "❌ Indicators"
            }

        df_d = df_d.dropna(
            subset=required_d
        )

        df_w = df_w.dropna(
            subset=[
                "ema200"
            ]
        )

        df_m = df_m.dropna(
            subset=[
                "ema200"
            ]
        )

        if (
            len(df_d) < 50 or
            len(df_w) < 50 or
            len(df_m) < 50
        ):
            return {
                "Symbol": clean_symbol,
                "Status": "❌ Insufficient"
            }

        last_d = df_d.iloc[-1]
        last_w = df_w.iloc[-1]
        last_m = df_m.iloc[-1]

        # -------------------------
        # Liquidity
        # -------------------------

        avg_value = float(
            last_d[
                "avg_traded_value"
            ]
        )

        liquidity = liquidity_score(
            last_d
        )

        liquidity_status = (
            "PASS"
            if avg_value >= min_liquidity
            else "LOW"
        )

        # -------------------------
        # Relative Strength
        # -------------------------

        rs_score, rs_pct = (
            calculate_relative_strength(
                df_d,
                benchmark
            )
        )

        # -------------------------
        # Technical
        # -------------------------

        technical = technical_score(
            last_d,
            last_w,
            last_m
        )

        # -------------------------
        # Sector
        # -------------------------

        sector = SECTORS.get(
            symbol,
            "Other"
        )

        sector_score = sector_scores.get(
            sector,
            50
        )

        # -------------------------
        # Trade plan
        # -------------------------

        plan = trade_plan(
            df_d,
            technical
        )

        rr_score = min(
            100,
            max(
                0,
                plan["RR_TP2"] /
                3 *
                100
            )
        )

        # -------------------------
        # Backtest
        # -------------------------

        bt = backtest_stock(
            df_d,
            backtest_horizon
        )

        # -------------------------
        # Final Score
        # -------------------------

        final = final_score(
            technical,
            liquidity,
            rs_score,
            sector_score,
            rr_score,
            bt["BT_Confidence"]
        )

        # If liquidity below threshold:
        # don't completely delete stock,
        # but flag it clearly.
        if avg_value < min_liquidity:

            final *= 0.80

        final = round(
            final,
            2
        )

        signal = signal_from_score(
            final
        )

        # -------------------------
        # Regime
        # -------------------------

        regime = market_regime(
            last_d
        )

        # -------------------------
        # ATR
        # -------------------------

        atr_pct = (
            last_d["atr"] /
            last_d["Close"] *
            100
        )

        # -------------------------
        # Time
        # -------------------------

        time_est = time_estimation(
            atr_pct
        )

        return {

            "Symbol":
                clean_symbol,

            "Status":
                "✅ OK",

            "Sector":
                sector,

            "Score":
                final,

            "Signal":
                signal,

            "Regime":
                regime,

            # ---------------------
            # Trade
            # ---------------------

            "Entry":
                round(
                    plan["Entry"],
                    2
                ),

            "SL":
                round(
                    plan["SL"],
                    2
                ),

            "TP1":
                round(
                    plan["TP1"],
                    2
                ),

            "TP2":
                round(
                    plan["TP2"],
                    2
                ),

            "TP3":
                round(
                    plan["TP3"],
                    2
                ),

            "RR_TP1":
                round(
                    plan["RR_TP1"],
                    2
                ),

            "RR_TP2":
                round(
                    plan["RR_TP2"],
                    2
                ),

            "RR_TP3":
                round(
                    plan["RR_TP3"],
                    2
                ),

            # ---------------------
            # Technical
            # ---------------------

            "Technical":
                round(
                    technical,
                    1
                ),

            "RSI":
                round(
                    float(
                        last_d["rsi"]
                    ),
                    2
                ),

            "ADX":
                round(
                    float(
                        last_d["adx"]
                    ),
                    2
                ),

            "ATR_%":
                round(
                    atr_pct,
                    2
                ),

            "MACD_Hist":
                round(
                    float(
                        last_d[
                            "macd_hist"
                        ]
                    ),
                    4
                ),

            # ---------------------
            # Liquidity
            # ---------------------

            "Liquidity":
                round(
                    liquidity,
                    1
                ),

            "Avg_Value_EGP":
                round(
                    avg_value,
                    0
                ),

            "Volume_Ratio":
                round(
                    float(
                        last_d[
                            "volume_ratio"
                        ]
                    ),
                    2
                ),

            "Liquidity_Status":
                liquidity_status,

            # ---------------------
            # Relative Strength
            # ---------------------

            "RS_Score":
                round(
                    rs_score,
                    1
                ),

            "RS_vs_EGX30_%":
                round(
                    rs_pct,
                    2
                ),

            # ---------------------
            # Sector
            # ---------------------

            "Sector_Score":
                round(
                    sector_score,
                    1
                ),

            # ---------------------
            # Backtest
            # ---------------------

            "BT_Trades":
                bt["BT_Trades"],

            "BT_WinRate_%":
                round(
                    bt["BT_WinRate"],
                    1
                ),

            "BT_AvgReturn_%":
                round(
                    bt["BT_AvgReturn"],
                    2
                ),

            "BT_Confidence_%":
                round(
                    bt["BT_Confidence"],
                    1
                ),

            "Time_Est":
                time_est
        }

    except Exception as e:

        return {
            "Symbol":
                clean_symbol,

            "Status":
                f"❌ {str(e)[:100]}"
        }


# =========================================================
# 📊 BENCHMARK LOADER
# =========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def load_benchmark(
    period
):

    candidates = [
        "^CASE30",
        "^EGX30",
        "EGX30.CA"
    ]

    for symbol in candidates:

        try:

            data = yf.download(
                symbol,
                period=period,
                interval="1d",
                auto_adjust=True,
                progress=False
            )

            if (
                data is not None and
                not data.empty
            ):

                if isinstance(
                    data.columns,
                    pd.MultiIndex
                ):
                    data.columns = (
                        data.columns
                        .get_level_values(0)
                    )

                if "Close" in data.columns:

                    return data[
                        ["Close"]
                    ].dropna()

        except Exception:
            continue

    return pd.DataFrame()


# =========================================================
# 🚀 RUN
# =========================================================

if st.button(
    "🚀 RUN EGX AI PRO MAX V6",
    use_container_width=True
):

    st.info(
        f"📡 جاري فحص {len(EGX100)} رمز..."
    )

    progress = st.progress(0)

    status = st.empty()

    # =====================================================
    # DOWNLOAD DAILY
    # =====================================================

    status.info(
        "📥 تحميل البيانات اليومية..."
    )

    daily = load_data(
        EGX100,
        period_daily,
        "1d"
    )

    progress.progress(15)

    # =====================================================
    # DOWNLOAD WEEKLY
    # =====================================================

    status.info(
        "📥 تحميل البيانات الأسبوعية..."
    )

    weekly = load_data(
        EGX100,
        period_weekly,
        "1wk"
    )

    progress.progress(30)

    # =====================================================
    # DOWNLOAD MONTHLY
    # =====================================================

    status.info(
        "📥 تحميل البيانات الشهرية..."
    )

    monthly = load_data(
        EGX100,
        period_monthly,
        "1mo"
    )

    progress.progress(45)

    # =====================================================
    # BENCHMARK
    # =====================================================

    status.info(
        "📊 تحميل Benchmark EGX30..."
    )

    benchmark = load_benchmark(
        period_daily
    )

    progress.progress(50)

    # =====================================================
    # PREPARE DATA FOR SECTORS
    # =====================================================

    status.info(
        "🏭 حساب أداء القطاعات..."
    )

    daily_dict = {}

    for symbol in EGX100:

        temp = extract_symbol_data(
            daily,
            symbol
        )

        if not temp.empty:

            daily_dict[
                symbol
            ] = temp

    sector_scores = (
        calculate_sector_scores(
            daily_dict
        )
    )

    # =====================================================
    # PARALLEL ANALYSIS
    # =====================================================

    results = []

    status.info(
        f"🧠 تحليل {len(EGX100)} سهم..."
    )

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        futures = {

            executor.submit(
                process_stock,
                symbol,
                daily,
                weekly,
                monthly,
                benchmark,
                sector_scores,
                min_liquidity,
                backtest_horizon
            ): symbol

            for symbol in EGX100
        }

        completed = 0

        for future in as_completed(
            futures
        ):

            symbol = futures[
                future
            ]

            try:

                result = future.result()

                if result:
                    results.append(
                        result
                    )

            except Exception as e:

                results.append({

                    "Symbol":
                        symbol.replace(
                            ".CA",
                            ""
                        ),

                    "Status":
                        f"❌ {str(e)[:100]}"
                })

            completed += 1

            progress.progress(
                50 +
                int(
                    completed /
                    len(EGX100) *
                    50
                )
            )

    progress.progress(100)

    status.success(
        "✅ انتهى الفحص بالكامل"
    )

    # =====================================================
    # DATAFRAME
    # =====================================================

    if not results:

        st.error(
            "❌ مفيش نتائج."
        )

        st.stop()

    df_all = pd.DataFrame(
        results
    )

    # =====================================================
    # COVERAGE
    # =====================================================

    total_requested = len(
        EGX100
    )

    analyzed = int(
        (
            df_all["Status"] ==
            "✅ OK"
        ).sum()
    )

    failed = (
        total_requested -
        analyzed
    )

    coverage = (
        analyzed /
        total_requested *
        100
        if total_requested
        else 0
    )

    # =====================================================
    # TOP METRICS
    # =====================================================

    st.subheader(
        "📡 Data Coverage"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Universe",
        total_requested
    )

    c2.metric(
        "Analyzed",
        analyzed
    )

    c3.metric(
        "Failed",
        failed
    )

    c4.metric(
        "Coverage",
        f"{coverage:.1f}%"
    )

    c5.metric(
        "Benchmark",
        "OK"
        if not benchmark.empty
        else "FAILED"
    )

    # =====================================================
    # VALID RESULTS
    # =====================================================

    df_ok = df_all[
        df_all["Status"] ==
        "✅ OK"
    ].copy()

    if df_ok.empty:

        st.error(
            "❌ مفيش سهم نجح في التحليل."
        )

        st.stop()

    # =====================================================
    # SORT
    # =====================================================

    df_ok = df_ok.sort_values(
        "Score",
        ascending=False
    )

    # =====================================================
    # 🏆 TOP STOCKS
    # =====================================================

    st.subheader(
        f"🏆 أفضل {min(top_n, len(df_ok))} سهم"
    )

    display_cols = [

        "Symbol",
        "Sector",
        "Score",
        "Signal",
        "Regime",

        "Entry",
        "SL",
        "TP1",
        "TP2",
        "TP3",

        "RR_TP1",
        "RR_TP2",
        "RR_TP3",

        "Technical",
        "Liquidity",
        "Avg_Value_EGP",
        "RS_Score",
        "RS_vs_EGX30_%",

        "Sector_Score",

        "BT_Trades",
        "BT_WinRate_%",
        "BT_Confidence_%",

        "RSI",
        "ADX",
        "ATR_%",

        "Time_Est"
    ]

    display_cols = [
        c for c in display_cols
        if c in df_ok.columns
    ]

    top_df = df_ok.head(
        top_n
    )

    st.dataframe(
        top_df[
            display_cols
        ],
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # 🔥 STRONG
    # =====================================================

    strong = df_ok[
        df_ok["Score"] >=
        min_score
    ].copy()

    st.subheader(
        f"🔥 فرص Score ≥ {min_score}: {len(strong)}"
    )

    if not strong.empty:

        st.dataframe(
            strong[
                display_cols
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "⚠️ مفيش أسهم وصلت للحد المطلوب."
        )

    # =====================================================
    # 🏭 BEST STOCK PER SECTOR
    # =====================================================

    st.subheader(
        "🏭 أفضل سهم في كل قطاع"
    )

    sector_best = (
        df_ok
        .sort_values(
            "Score",
            ascending=False
        )
        .groupby(
            "Sector",
            as_index=False
        )
        .first()
        .sort_values(
            "Score",
            ascending=False
        )
    )

    st.dataframe(
        sector_best[
            [
                "Sector",
                "Symbol",
                "Score",
                "Signal",
                "Technical",
                "Liquidity",
                "RS_Score",
                "Sector_Score",
                "BT_Confidence_%",
                "RR_TP2"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # 🏭 SECTOR RANKING
    # =====================================================

    st.subheader(
        "📊 Sector Ranking"
    )

    sector_ranking = (
        df_ok
        .groupby("Sector")
        .agg(
            Stocks=("Symbol", "count"),
            AvgScore=("Score", "mean"),
            AvgLiquidity=("Liquidity", "mean"),
            AvgRS=("RS_Score", "mean"),
            AvgBTConfidence=(
                "BT_Confidence_%",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "AvgScore",
            ascending=False
        )
    )

    sector_ranking[
        "AvgScore"
    ] = sector_ranking[
        "AvgScore"
    ].round(2)

    sector_ranking[
        "AvgLiquidity"
    ] = sector_ranking[
        "AvgLiquidity"
    ].round(2)

    sector_ranking[
        "AvgRS"
    ] = sector_ranking[
        "AvgRS"
    ].round(2)

    sector_ranking[
        "AvgBTConfidence"
    ] = sector_ranking[
        "AvgBTConfidence"
    ].round(2)

    st.dataframe(
        sector_ranking,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # 💧 LIQUIDITY LEADERS
    # =====================================================

    st.subheader(
        "💧 Liquidity Leaders"
    )

    liquidity_df = (
        df_ok
        .sort_values(
            "Avg_Value_EGP",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        liquidity_df[
            [
                "Symbol",
                "Sector",
                "Score",
                "Liquidity",
                "Avg_Value_EGP",
                "Volume_Ratio",
                "Signal"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # 📈 RELATIVE STRENGTH LEADERS
    # =====================================================

    st.subheader(
        "📈 Relative Strength Leaders vs EGX30"
    )

    rs_df = (
        df_ok
        .sort_values(
            "RS_Score",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        rs_df[
            [
                "Symbol",
                "Sector",
                "Score",
                "RS_Score",
                "RS_vs_EGX30_%",
                "Signal"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # 🧪 BACKTEST LEADERS
    # =====================================================

    st.subheader(
        "🧪 Backtest Leaders"
    )

    bt_df = (
        df_ok[
            df_ok["BT_Trades"] >= 5
        ]
        .sort_values(
            [
                "BT_Confidence_%",
                "BT_WinRate_%"
            ],
            ascending=False
        )
        .head(20)
    )

    if not bt_df.empty:

        st.dataframe(
            bt_df[
                [
                    "Symbol",
                    "Sector",
                    "Score",
                    "BT_Trades",
                    "BT_WinRate_%",
                    "BT_AvgReturn_%",
                    "BT_Confidence_%"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "⚠️ مفيش عدد كافي من صفقات الـ Backtest."
        )

    # =====================================================
    # ⚠️ LOW LIQUIDITY
    # =====================================================

    low_liq = df_ok[
        df_ok[
            "Liquidity_Status"
        ] == "LOW"
    ].copy()

    st.subheader(
        f"⚠️ أسهم السيولة الضعيفة: {len(low_liq)}"
    )

    if not low_liq.empty:

        st.dataframe(
            low_liq[
                [
                    "Symbol",
                    "Sector",
                    "Score",
                    "Avg_Value_EGP",
                    "Liquidity_Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # 📋 ALL ANALYZED
    # =====================================================

    st.subheader(
        "📋 جميع الأسهم المحللة"
    )

    st.dataframe(
        df_ok[
            display_cols
        ],
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # ❌ FAILED
    # =====================================================

    df_failed = df_all[
        df_all["Status"] != "✅ OK"
    ].copy()

    st.subheader(
        f"❌ الأسهم الفاشلة: {len(df_failed)}"
    )

    if not df_failed.empty:

        st.dataframe(
            df_failed[
                [
                    "Symbol",
                    "Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # 📥 DOWNLOAD FULL
    # =====================================================

    csv_all = df_ok.to_csv(
        index=False
    ).encode(
        "utf-8-sig"
    )

    st.download_button(
        "⬇️ تحميل كل النتائج CSV",
        csv_all,
        "EGX_AI_PRO_MAX_V6_ALL.csv",
        "text/csv",
        use_container_width=True
    )

    # =====================================================
    # 📥 DOWNLOAD TOP
    # =====================================================

    csv_top = top_df.to_csv(
        index=False
    ).encode(
        "utf-8-sig"
    )

    st.download_button(
        "⬇️ تحميل أفضل الأسهم CSV",
        csv_top,
        "EGX_AI_PRO_MAX_V6_TOP.csv",
        "text/csv",
        use_container_width=True
    )

    # =====================================================
    # 📥 DOWNLOAD SECTORS
    # =====================================================

    csv_sector = sector_best.to_csv(
        index=False
    ).encode(
        "utf-8-sig"
    )

    st.download_button(
        "⬇️ تحميل أفضل سهم لكل قطاع",
        csv_sector,
        "EGX_AI_PRO_MAX_V6_SECTORS.csv",
        "text/csv",
        use_container_width=True
    )

    # =====================================================
    # 📥 DOWNLOAD ERRORS
    # =====================================================

    if not df_failed.empty:

        csv_failed = (
            df_failed
            .to_csv(
                index=False
            )
            .encode(
                "utf-8-sig"
            )
        )

        st.download_button(
            "⬇️ تحميل الأخطاء",
            csv_failed,
            "EGX_AI_PRO_MAX_V6_ERRORS.csv",
            "text/csv",
            use_container_width=True
        )

    # =====================================================
    # FINAL SUMMARY
    # =====================================================

    avg_score = round(
        df_ok["Score"].mean(),
        2
    )

    avg_bt = round(
        df_ok[
            "BT_Confidence_%"
        ].mean(),
        2
    )

    st.success(
        f"""
🔥 EGX AI PRO MAX V6 اكتمل

📊 الكون المطلوب: {total_requested}

✅ تم التحليل: {analyzed}

❌ فشل: {failed}

📡 Data Coverage: {coverage:.1f}%

⭐ متوسط Final Score: {avg_score}

🧪 متوسط Backtest Confidence: {avg_bt}%

🏆 أفضل سهم:
{df_ok.iloc[0]["Symbol"]}

📈 Score:
{df_ok.iloc[0]["Score"]}
"""
    )

    # =====================================================
    # DISCLAIMER
    # =====================================================

    st.caption(
        "⚠️ الـ Backtest تاريخي وليس ضمانًا للنتائج المستقبلية. "
        "الـ Confidence هنا مبني على نتائج تاريخية داخل البيانات المتاحة، "
        "وليس توقعًا مضمونًا."
)
