import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import ta
from concurrent.futures import ThreadPoolExecutor, as_completed

# =========================================================
# ⚙️ إعداد الصفحة
# =========================================================

st.set_page_config(
    page_title="EGX AI PRO MAX v6 - عربي",
    page_icon="📈",
    layout="wide"
)

st.title("🚀 EGX AI PRO MAX v6")
st.caption("📊 فحص الأسهم المصرية • تحليل متعدد الفترات • تقييم ذكي • محرك بيانات سريع")

# =========================================================
# 📌 قائمة الأسهم
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
    "MPCO.CA", "ELSH.CA", "NCCW.CA", "MEPA.CA", "ODIN.CA",
    "EGAS.CA", "MENA.CA", "RACC.CA", "PRCL.CA", "BINV.CA",
    "EDBM.CA", "MCQE.CA", "MOIL.CA", "NIPH.CA", "ISPH.CA",
    "DICE.CA", "BINV.CA", "IDHC.CA", "UNIT.CA", "PHAR.CA",
    "TRTO.CA", "ALRA.CA", "FARE.CA", "ICFC.CA", "MISr.CA",
    "MOBI.CA", "RACC.CA", "ELKA.CA", "NILE.CA", "ATLC.CA",
    "COSG.CA", "MEDA.CA", "ELSH.CA", "AMPI.CA", "COPR.CA"
]

# إزالة التكرارات
EGX100 = list(dict.fromkeys(EGX100))

TOTAL_STOCKS = len(EGX100)

# =========================================================
# 🎛️ إعدادات الفحص
# =========================================================

st.sidebar.header("⚙️ إعدادات الفحص")

period_daily = st.sidebar.selectbox(
    "📅 فترة البيانات اليومية",
    ["3mo", "6mo", "1y", "2y", "3y", "5y"],
    index=1
)

period_weekly = st.sidebar.selectbox(
    "📅 فترة البيانات الأسبوعية",
    ["1y", "2y", "3y", "5y"],
    index=1
)

period_monthly = st.sidebar.selectbox(
    "📅 فترة البيانات الشهرية",
    ["3y", "5y", "10y", "max"],
    index=1
)

max_workers = st.sidebar.slider(
    "⚡ عدد الاتصالات المتوازية",
    min_value=2,
    max_value=16,
    value=8,
    step=1
)

top_n = st.sidebar.slider(
    "🏆 عدد أفضل الأسهم",
    min_value=5,
    max_value=100,
    value=20,
    step=5
)

st.sidebar.markdown("---")

st.sidebar.metric(
    "📊 عدد الأسهم للفحص",
    TOTAL_STOCKS
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    📌 النظام يقوم بفحص:

    • الاتجاه اليومي
    • الاتجاه الأسبوعي
    • الاتجاه الشهري
    • EMA20
    • EMA50
    • EMA200
    • RSI
    • MACD
    • Volume
    • OBV
    • ATR
    • ADX
    • الدعم والمقاومة
    • التقييم النهائي
    • الدخول
    • وقف الخسارة
    • 3 أهداف
    """
)

# =========================================================
# 📊 تحميل البيانات
# =========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def load_data(symbols, period, interval):

    if not symbols:
        return pd.DataFrame()

    try:

        data = yf.download(
            tickers=symbols,
            period=period,
            interval=interval,
            group_by="ticker",
            threads=True,
            auto_adjust=True,
            progress=False
        )

        return data

    except Exception:

        return None


# =========================================================
# 🔍 استخراج بيانات السهم
# =========================================================

def extract_symbol_data(data, symbol):

    try:

        if data is None or data.empty:
            return pd.DataFrame()

        # MultiIndex
        if isinstance(data.columns, pd.MultiIndex):

            if symbol in data.columns.get_level_values(0):

                df = data[symbol].copy()

            elif symbol in data.columns.get_level_values(1):

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

        available = [
            c for c in required
            if c in df.columns
        ]

        if len(available) < 5:
            return pd.DataFrame()

        df = df[available].copy()

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
# 📈 المؤشرات الفنية
# =========================================================

def add_indicators(df):

    df = df.copy()

    if len(df) < 50:
        return df

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    vol = df["Volume"]

    # -----------------------------------------------------
    # EMA
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # RSI
    # -----------------------------------------------------

    df["rsi"] = ta.momentum.RSIIndicator(
        close=close,
        window=14
    ).rsi()

    # -----------------------------------------------------
    # MACD
    # -----------------------------------------------------

    macd_obj = ta.trend.MACD(
        close=close,
        window_slow=26,
        window_fast=12,
        window_sign=9
    )

    df["macd"] = macd_obj.macd()

    df["macd_signal"] = (
        macd_obj.macd_signal()
    )

    df["macd_hist"] = (
        macd_obj.macd_diff()
    )

    # -----------------------------------------------------
    # Volume
    # -----------------------------------------------------

    df["vol_ma"] = vol.rolling(
        20
    ).mean()

    # -----------------------------------------------------
    # Support / Resistance
    # -----------------------------------------------------

    df["support"] = low.rolling(
        20
    ).min()

    df["resistance"] = high.rolling(
        20
    ).max()

    # -----------------------------------------------------
    # OBV
    # -----------------------------------------------------

    try:

        df["obv"] = (
            ta.volume
            .OnBalanceVolumeIndicator(
                close=close,
                volume=vol
            )
            .on_balance_volume()
        )

    except Exception:

        df["obv"] = np.nan

    return df


# =========================================================
# 📊 ATR
# =========================================================

def atr(df, period=14):

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ],
        axis=1
    ).max(axis=1)

    return tr.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()


# =========================================================
# 📊 ADX
# =========================================================

def adx(df, period=14):

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    plus_dm_raw = high.diff()

    minus_dm_raw = -low.diff()

    plus_dm = np.where(
        (plus_dm_raw > minus_dm_raw) &
        (plus_dm_raw > 0),
        plus_dm_raw,
        0.0
    )

    minus_dm = np.where(
        (minus_dm_raw > plus_dm_raw) &
        (minus_dm_raw > 0),
        minus_dm_raw,
        0.0
    )

    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ],
        axis=1
    ).max(axis=1)

    atr_val = tr.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    plus_di = (
        100 *
        pd.Series(
            plus_dm,
            index=df.index
        ).ewm(
            alpha=1 / period,
            adjust=False
        ).mean()
        /
        (atr_val + 1e-9)
    )

    minus_di = (
        100 *
        pd.Series(
            minus_dm,
            index=df.index
        ).ewm(
            alpha=1 / period,
            adjust=False
        ).mean()
        /
        (atr_val + 1e-9)
    )

    dx = (
        abs(
            plus_di -
            minus_di
        )
        /
        (
            plus_di +
            minus_di +
            1e-9
        )
    ) * 100

    return dx.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()


# =========================================================
# 🧠 تحديد اتجاه السهم
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

    if score >= 4:

        return "🚀 قوي جداً"

    elif score == 3:

        return "🟢 صعود"

    elif score == 2:

        return "🟡 محايد"

    else:

        return "🔴 هبوط"


# =========================================================
# 🧠 محرك الثقة
# =========================================================

def ai_confidence(
    last_d,
    last_w,
    last_m,
    adx_val,
    atr_val
):

    score = 0

    total = 8

    if last_d["Close"] > last_d["ema200"]:
        score += 1

    if last_w["Close"] > last_w["ema200"]:
        score += 1

    if last_m["Close"] > last_m["ema200"]:
        score += 1

    if last_d["macd"] > 0:
        score += 1

    if 45 < last_d["rsi"] < 65:
        score += 1

    if last_d["Volume"] > last_d["vol_ma"]:
        score += 1

    if adx_val > 20:
        score += 1

    if (
        atr_val /
        last_d["Close"]
    ) < 0.05:

        score += 1

    return score / total


# =========================================================
# 🧠 التحليل الرئيسي
# =========================================================

def analyze(
    df_d,
    df_w,
    df_m
):

    # إضافة المؤشرات

    df_d = add_indicators(df_d)
    df_w = add_indicators(df_w)
    df_m = add_indicators(df_m)

    # -----------------------------------------------------
    # التأكد من البيانات
    # -----------------------------------------------------

    if (
        len(df_d) < 50 or
        len(df_w) < 50 or
        len(df_m) < 50
    ):

        raise ValueError(
            "بيانات غير كافية"
        )

    # -----------------------------------------------------
    # تنظيف المؤشرات
    # -----------------------------------------------------

    df_d = df_d.dropna(
        subset=[
            "ema200",
            "rsi",
            "macd",
            "vol_ma",
            "support",
            "resistance"
        ]
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
        df_d.empty or
        df_w.empty or
        df_m.empty
    ):

        raise ValueError(
            "المؤشرات غير متاحة"
        )

    # -----------------------------------------------------
    # آخر قراءة
    # -----------------------------------------------------

    last_d = df_d.iloc[-1]

    last_w = df_w.iloc[-1]

    last_m = df_m.iloc[-1]

    entry = float(
        last_d["Close"]
    )

    if entry <= 0:

        raise ValueError(
            "سعر غير صحيح"
        )

    # -----------------------------------------------------
    # ATR
    # -----------------------------------------------------

    atr_val = float(
        atr(df_d).iloc[-1]
    )

    # -----------------------------------------------------
    # ADX
    # -----------------------------------------------------

    adx_val = float(
        adx(df_d).iloc[-1]
    )

    if not np.isfinite(
        atr_val
    ):

        raise ValueError(
            "ATR غير صحيح"
        )

    if not np.isfinite(
        adx_val
    ):

        adx_val = 0

    # =====================================================
    # ⭐ التقييم
    # =====================================================

    score = 0

    # الاتجاه اليومي

    if (
        last_d["Close"] >
        last_d["ema200"]
    ):

        score += 15

    # الاتجاه الأسبوعي

    if (
        last_w["Close"] >
        last_w["ema200"]
    ):

        score += 12

    # الاتجاه الشهري

    if (
        last_m["Close"] >
        last_m["ema200"]
    ):

        score += 15

    # RSI

    if (
        45 <
        last_d["rsi"] <
        65
    ):

        score += 8

    # MACD

    if last_d["macd"] > 0:

        score += 6

    # Volume

    if (
        last_d["Volume"] >
        last_d["vol_ma"]
    ):

        score += 8

    # ADX

    if adx_val > 20:

        score += 10

    # الاتجاه العام

    regime = market_regime(
        last_d
    )

    if "قوي" in regime:

        score += 6

    # المخاطرة

    volatility = (
        atr_val /
        entry
    )

    if volatility < 0.05:

        score += 5

    else:

        score -= 5

    # =====================================================
    # 🎯 الأهداف
    # =====================================================

    support = float(
        last_d["support"]
    )

    resistance = float(
        last_d["resistance"]
    )

    ema_trend = (
        float(last_d["ema20"]) -
        float(last_d["ema200"])
    ) / entry

    adx_strength = min(
        1.0,
        max(
            0.0,
            adx_val / 100
        )
    )

    # -----------------------------------------------------
    # الهدف الأول
    # -----------------------------------------------------

    if ema_trend > 0:

        tp1 = (
            entry +
            atr_val * 0.8
        )

    else:

        tp1 = (
            entry -
            atr_val * 0.8
        )

    # -----------------------------------------------------
    # الهدف الثاني
    # -----------------------------------------------------

    tp2_multiplier = (
        1.8 +
        adx_strength * 2
    )

    if ema_trend > 0:

        tp2 = (
            entry +
            atr_val *
            tp2_multiplier
        )

    else:

        tp2 = (
            entry -
            atr_val *
            tp2_multiplier
        )

    # -----------------------------------------------------
    # الهدف الثالث
    # -----------------------------------------------------

    trend_multiplier = (
        3 +
        adx_strength * 4 +
        abs(ema_trend) * 10
    )

    if ema_trend > 0:

        tp3 = max(
            resistance,
            entry +
            atr_val *
            trend_multiplier
        )

    else:

        tp3 = min(
            support,
            entry -
            atr_val *
            trend_multiplier
        )

    # =====================================================
    # 🛑 وقف الخسارة
    # =====================================================

    if ema_trend > 0:

        stop = (
            entry -
            atr_val *
            (
                1.2 +
                volatility * 5
            )
        )

    else:

        stop = (
            entry +
            atr_val *
            (
                1.2 +
                volatility * 5
            )
        )

    # =====================================================
    # ⏱️ المدة المتوقعة
    # =====================================================

    if volatility > 0.05:

        time_est = "1 - 3 أسابيع"

    elif volatility > 0.02:

        time_est = "3 - 8 أسابيع"

    else:

        time_est = "2 - 4 شهور"

    # =====================================================
    # 🧠 الاحتمالات
    # =====================================================

    base_conf = ai_confidence(
        last_d,
        last_w,
        last_m,
        adx_val,
        atr_val
    )

    momentum_factor = min(
        1.2,
        max(
            0.5,
            adx_val / 25
        )
    )

    trend_factor = min(
        1.2,
        1 +
        abs(ema_trend) * 5
    )

    vol_factor = (
        1 -
        min(
            0.5,
            volatility
        )
    )

    tp1_prob = min(
        0.95,
        base_conf *
        momentum_factor *
        trend_factor *
        vol_factor
    )

    tp2_prob = min(
        0.90,
        tp1_prob *
        (
            0.85 +
            adx_strength
        )
    )

    tp3_prob = min(
        0.85,
        tp2_prob *
        (
            0.75 +
            abs(ema_trend) * 3
        )
    )

    # =====================================================
    # 🚦 الإشارة
    # =====================================================

    if score > 85:

        signal = "🔥 قوي جداً"

    elif score > 70:

        signal = "🟢 قوي"

    elif score >= 55:

        signal = "🟡 متوسط"

    else:

        signal = "⚠️ متابعة"

    # =====================================================
    # 📦 النتيجة
    # =====================================================

    return {

        "التقييم": round(
            score,
            2
        ),

        "الإشارة": signal,

        "الاتجاه": regime,

        "سعر الدخول": round(
            entry,
            2
        ),

        "وقف الخسارة": round(
            stop,
            2
        ),

        "الهدف الأول": round(
            tp1,
            2
        ),

        "الهدف الثاني": round(
            tp2,
            2
        ),

        "الهدف الثالث": round(
            tp3,
            2
        ),

        "احتمال الهدف الأول %": round(
            tp1_prob * 100,
            1
        ),

        "احتمال الهدف الثاني %": round(
            tp2_prob * 100,
            1
        ),

        "احتمال الهدف الثالث %": round(
            tp3_prob * 100,
            1
        ),

        "التذبذب ATR %": round(
            volatility * 100,
            2
        ),

        "قوة الاتجاه ADX": round(
            adx_val,
            2
        ),

        "مؤشر RSI": round(
            float(last_d["rsi"]),
            2
        ),

        "المدة المتوقعة": time_est
    }


# =========================================================
# ⚡ معالجة سهم واحد
# =========================================================

def process(
    symbol,
    daily,
    weekly,
    monthly
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
                "السهم": clean_symbol,
                "الحالة": "❌ لا توجد بيانات يومية"
            }

        if df_w.empty:

            return {
                "السهم": clean_symbol,
                "الحالة": "❌ لا توجد بيانات أسبوعية"
            }

        if df_m.empty:

            return {
                "السهم": clean_symbol,
                "الحالة": "❌ لا توجد بيانات شهرية"
            }

        result = analyze(
            df_d,
            df_w,
            df_m
        )

        result["السهم"] = clean_symbol

        result["الحالة"] = "✅ تم التحليل"

        return result

    except Exception as e:

        return {
            "السهم": clean_symbol,
            "الحالة": f"❌ {str(e)[:80]}"
        }


# =========================================================
# 🚀 تشغيل الفحص
# =========================================================

if st.button(
    "🚀 بدء فحص الأسهم",
    use_container_width=True
):

    # -----------------------------------------------------
    # الحالة
    # -----------------------------------------------------

    st.info(
        f"📡 جاري فحص {TOTAL_STOCKS} سهم..."
    )

    progress = st.progress(
        0
    )

    status_text = st.empty()

    # =====================================================
    # 📥 البيانات اليومية
    # =====================================================

    with st.spinner(
        "📥 جاري تحميل البيانات اليومية..."
    ):

        daily = load_data(
            EGX100,
            period_daily,
            "1d"
        )

    progress.progress(
        20
    )

    # =====================================================
    # 📥 البيانات الأسبوعية
    # =====================================================

    status_text.info(
        "📥 جاري تحميل البيانات الأسبوعية..."
    )

    weekly = load_data(
        EGX100,
        period_weekly,
        "1wk"
    )

    progress.progress(
        40
    )

    # =====================================================
    # 📥 البيانات الشهرية
    # =====================================================

    status_text.info(
        "📥 جاري تحميل البيانات الشهرية..."
    )

    monthly = load_data(
        EGX100,
        period_monthly,
        "1mo"
    )

    progress.progress(
        50
    )

    # =====================================================
    # 🧠 التحليل
    # =====================================================

    results = []

    status_text.info(
        f"🧠 جاري تحليل {TOTAL_STOCKS} سهم بالتوازي..."
    )

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        futures = {
            executor.submit(
                process,
                symbol,
                daily,
                weekly,
                monthly
            ): symbol

            for symbol in EGX100
        }

        completed = 0

        for future in as_completed(
            futures
        ):

            try:

                result = future.result()

                if result:

                    results.append(
                        result
                    )

            except Exception as e:

                symbol = futures[
                    future
                ]

                results.append({

                    "السهم":
                        symbol.replace(
                            ".CA",
                            ""
                        ),

                    "الحالة":
                        f"❌ {str(e)[:80]}"
                })

            completed += 1

            progress.progress(
                50 +
                int(
                    completed /
                    TOTAL_STOCKS *
                    50
                )
            )

    progress.progress(
        100
    )

    status_text.success(
        "✅ انتهى الفحص بالكامل"
    )

    # =====================================================
    # 📊 النتائج
    # =====================================================

    if not results:

        st.error(
            "❌ لم يتم الحصول على أي نتائج."
        )

        st.stop()

    df_all = pd.DataFrame(
        results
    )

    # =====================================================
    # 📊 التغطية
    # =====================================================

    total = TOTAL_STOCKS

    analyzed = int(
        (
            df_all["الحالة"] ==
            "✅ تم التحليل"
        ).sum()
    )

    failed = total - analyzed

    coverage = (
        analyzed /
        total *
        100
        if total > 0
        else 0
    )

    # =====================================================
    # 📊 مؤشرات عامة
    # =====================================================

    st.subheader(
        "📊 ملخص الفحص"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📊 الأسهم المطلوبة",
        total
    )

    c2.metric(
        "✅ تم تحليلها",
        analyzed
    )

    c3.metric(
        "❌ فشل",
        failed
    )

    c4.metric(
        "📡 نسبة التغطية",
        f"{coverage:.1f}%"
    )

    # =====================================================
    # 📈 الأسهم الناجحة
    # =====================================================

    df_ok = df_all[
        df_all["الحالة"] ==
        "✅ تم التحليل"
    ].copy()

    if not df_ok.empty:

        # ترتيب حسب التقييم

        df_ok = df_ok.sort_values(
            "التقييم",
            ascending=False
        )

        # =================================================
        # 🏆 أفضل الأسهم
        # =================================================

        st.subheader(
            f"🏆 أفضل {min(top_n, len(df_ok))} سهم"
        )

        top_df = df_ok.head(
            top_n
        ).copy()

        preferred_cols = [

            "السهم",

            "التقييم",

            "الإشارة",

            "الاتجاه",

            "سعر الدخول",

            "وقف الخسارة",

            "الهدف الأول",

            "الهدف الثاني",

            "الهدف الثالث",

            "احتمال الهدف الأول %",

            "احتمال الهدف الثاني %",

            "احتمال الهدف الثالث %",

            "مؤشر RSI",

            "قوة الاتجاه ADX",

            "التذبذب ATR %",

            "المدة المتوقعة"

        ]

        existing_cols = [

            c for c in preferred_cols
            if c in top_df.columns

        ]

        top_df = top_df[
            existing_cols
        ]

        st.dataframe(
            top_df,
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # 🔥 الأسهم القوية
        # =================================================

        strong = df_ok[
            df_ok["التقييم"] > 70
        ].copy()

        st.subheader(
            f"🔥 الأسهم القوية: {len(strong)}"
        )

        if not strong.empty:

            strong = strong[
                existing_cols
            ]

            st.dataframe(
                strong,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "⚠️ لا توجد أسهم قوية حالياً حسب شروط النظام."
            )

        # =================================================
        # 📋 جميع الأسهم المحللة
        # =================================================

        st.subheader(
            "📋 جميع الأسهم التي تم تحليلها"
        )

        st.dataframe(
            df_ok[
                existing_cols
            ],
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # 💾 تحميل النتائج
        # =================================================

        csv_ok = (
            df_ok
            .to_csv(
                index=False
            )
            .encode(
                "utf-8-sig"
            )
        )

        st.download_button(
            "⬇️ تحميل نتائج الأسهم المحللة",
            csv_ok,
            "EGX_AI_PRO_MAX_RESULTS_AR.csv",
            "text/csv",
            use_container_width=True
        )

    else:

        st.error(
            "❌ لم ينجح أي سهم في التحليل."
        )

    # =====================================================
    # ⚠️ الأسهم الفاشلة
    # =====================================================

    df_failed = df_all[
        df_all["الحالة"] !=
        "✅ تم التحليل"
    ].copy()

    if not df_failed.empty:

        st.subheader(
            f"⚠️ الأسهم التي فشل تحميل/تحليل بياناتها: {len(df_failed)}"
        )

        st.dataframe(
            df_failed[
                [
                    "السهم",
                    "الحالة"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

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
            "⬇️ تحميل قائمة الأخطاء",
            csv_failed,
            "EGX_AI_PRO_MAX_ERRORS_AR.csv",
            "text/csv",
            use_container_width=True
        )

    # =====================================================
    # 🏁 الحالة النهائية
    # =====================================================

    st.success(
        f"""
🔥 الفحص اكتمل بنجاح

📊 إجمالي الأسهم: {total}

✅ تم تحليل: {analyzed}

❌ فشل: {failed}

📡 نسبة تغطية البيانات: {coverage:.1f}%
"""
    )
