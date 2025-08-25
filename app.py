import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

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
from components.daily_candlestick_10 import show_candlestick_with_neutral
from components.short_interest_chart_11 import show_short_interest_chart
from components.exchange_summary_table_12 import show_exchange_summary_table

# === Load and Prepare Data ===
df_raw, df_full = load_and_prepare_data()

# === Global Filter (sidebar selector) ===
with st.sidebar:
    st.markdown("### 📅 Custom Analysis Period")
    st.markdown(
        "<p style='font-size: 0.9em; color: gray;'>Use the dropdown below to select the time period:</p>",
        unsafe_allow_html=True
    )
    df_filtered, period_label, start_date, end_date, period_key = get_analysis_period_filter(df_full)

# === Logo and Title ===
show_logo_and_centered_title(period_label)

# === Market Benchmarks Section ===
with st.container():
    st.markdown(f"""
        <div style="text-align: center; padding-bottom: 10px;">
            <h2 style='margin-bottom:5px;'>📌 Market Benchmarks</h2>
            <p style='color:gray; font-size:1.0em;'>
                <b>Reference Period:</b> {period_label}<br>
                Compared to the <b>previous {period_key.lower()}</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)  # spacer

# === Benchmarks Table ===
st.header("Variance by Period")
spec = [1, 8, 1]  # centraliza a tabela
col1, col2, col3 = st.columns(spec)
with col2:
    show_benchmarks_table(df_full)

# Divider
st.divider()

# === Selected Period Analysis Section ===
st.markdown(f"""
    <div style="text-align: center; padding-bottom: 10px;">
        <h2 style='margin-bottom:5px;'>🔍 Analysis for Selected Period</h2>
        <p style='color:gray; font-size:1.0em;'>
            <b>Selected Period:</b> {period_label}
        </p>
    </div>
""", unsafe_allow_html=True)

# === Components ===

# Price Bucket Summary
st.subheader("📊 Price Bucket Summary")
st.caption("Top 5 price buckets by volume for the selected period")
show_price_bucket_table(df_filtered, period_label, end_date)

# Exchange Distribution (Pie Chart)
st.subheader("Exchange Distribution")
show_exchange_pie_chart_altair(df_filtered, period_label, period_key, end_date)

# Exchange Summary
st.subheader("Exchange Summary")
show_exchange_summary_table(
    df_filtered,
    df_full,
    period_label,
    start_date,
    end_date,
    period_key
)



# Price & Volume Chart (linha + volume + SMA)
st.subheader("Price & Volume Trend")
show_price_volume_chart_plotly(df_full, start_date, end_date, period_label)

# Candlestick Chart
st.subheader("show_price_candlestick")
show_candlestick_with_neutral(df_full, start_date, end_date, period_label)

# Short Interest Section
st.subheader("Short Interest Evolution")

show_short_interest_chart(
    df_full,
    start_date,
    end_date,
    period_label)
