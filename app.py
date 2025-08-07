import streamlit as st

# === Page Config ===
st.set_page_config(page_title="ValOre Trading Insights", layout="wide")

# === Imports ===
from utils.data_loader import load_and_prepare_data
from components.logo_header_1 import show_logo_and_centered_title
from components.get_last_closed_week_2 import get_last_closed_week
from components.get_analysis_period_filter_3 import get_analysis_period_filter
from components.highlits_4 import show_highlights_block
from components.benchmarks_table_5 import show_benchmarks_table
from components.price_bucket_table_6 import show_price_bucket_table
from utils.top5_utils import get_top5_consolidated_df
from components.price_bucket_chart_7 import show_price_bucket_chart_from_consolidated
from components.exchange_pie_chart_8 import show_exchange_pie_chart_altair
from components.price_volume_chart_9 import show_price_volume_chart_plotly
from components.daily_candlestick_10 import show_candlestick_chart_plotly
from components.short_interest_chart_11 import show_short_interest_chart

# === Load and Prepare Data ===
df_raw, df_full = load_and_prepare_data()

# === Weekly Summary Section ===
df_filtered, period_label, start_week, end_week = get_last_closed_week(df_full)

# ✅ Render the logo and main title
show_logo_and_centered_title(period_label)

# === Weekly Highlights (título + KPIs juntos como uma seção unificada) ===
with st.container():
    st.markdown(f"""
        <div style="text-align: center; padding-bottom: 10px;">
            <h2 style='margin-bottom:5px;'>📌 Weekly Highlights</h2>
            <p style='color:gray; font-size:1.0em;'>
                <b>Reference Period:</b> {period_label}<br>
                Compared to the <b>previous week</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    spec = [1, 3, 1, 3, 1, 3, 1]
    col1, col2, col3, col4, col5, col6, col7 = st.columns(spec, gap="large", vertical_alignment="bottom", border=False)

    with col2:
        show_highlights_block(df_full, df_filtered, period_label, start_week, end_week, kpi="volume")
    with col4:
        show_highlights_block(df_full, df_filtered, period_label, start_week, end_week, kpi="bucket")
    with col6:
        show_highlights_block(df_full, df_filtered, period_label, start_week, end_week, kpi="vwap")

st.markdown(
    """
    <div style="margin-top: 50 px;"></div>
    """,
    unsafe_allow_html=True
)

# === Benchmarks Table ===
st.write("")
st.write("")  # repit por for space
st.header("Market Benchmarks – Last closed week")

spec = [1, 8, 1]  # col1 and col3 are margins, and col2 is the center
col1, col2, col3 = st.columns(spec)

with col2:
    show_benchmarks_table(df_full)

# === Sidebar: Period Selector ===
with st.sidebar:
    st.markdown("### 📅 Custom Analysis Period")
    st.markdown(
        "<p style='font-size: 0.9em; color: gray;'>Use the dropdown below to select a time period:</p>",
        unsafe_allow_html=True,
    )
    analysis_df, analysis_label, analysis_start, analysis_end = get_analysis_period_filter(df_full)


st.divider()

# === Section Title ===
st.markdown(f"""
    <div style="text-align: center; padding-bottom: 10px;">
        <h2 style='margin-bottom:5px;'>🔍 Analysis for Selected Period</h2>
        <p style='color:gray; font-size:1.0em;'>
            <b>Selected Period:</b> {analysis_label}
        </p>
    </div>
""", unsafe_allow_html=True)

# === Centralized Content ===

# Top 5 Buckets Table
st.write("")
st.write("")  # repit por for space
st.header("Price Bucket Summary")
show_price_bucket_table(analysis_df, analysis_label, analysis_end)

#Top 5 bucket chart
st.write("")
st.write("")  # repit por for space
st.header("Bid vs Ask – Top 5 Price Buckets")
df_consolidated = get_top5_consolidated_df(analysis_df)
show_price_bucket_chart_from_consolidated(df_consolidated, analysis_label, analysis_end)

#Exchance Distribution (Pie Chart)
st.write("")
st.write("")  # repit por for space
st.header("Exchange Distribution (Pie Chart)")
show_exchange_pie_chart_altair(df_raw, period_label=analysis_label)

#Price and Volume Chart
st.write("")
st.write("")  # repit por for space
st.header(" Price & Volume Over Time")
show_price_volume_chart_plotly(df_full, analysis_start, analysis_end, analysis_label)

#Candlestick-Chart-Plot
st.write("")
st.write("")  # repit por for space
st.header("Open & Close Price Candlestick")
show_candlestick_chart_plotly(df_full, analysis_start, analysis_end, analysis_label)

# Short interest
st.write("")
st.write("")  # repit por for space
st.header("Short Interest Over Time")

analysis_df, analysis_label, analysis_start, analysis_end = get_analysis_period_filter(df_full)

show_short_interest_chart(analysis_df, analysis_start, analysis_end, analysis_label)