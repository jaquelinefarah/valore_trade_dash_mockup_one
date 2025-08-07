import streamlit as st
import pandas as pd
import numpy as np

def load_raw_data():
    df_raw = pd.read_csv("data/valore_trade.csv")
    df_raw.columns = df_raw.columns.str.strip().str.lower().str.replace(" ", "_")
    df_raw["date"] = pd.to_datetime(df_raw["date"])
    return df_raw

def build_full_calendar(df_raw):
    min_date = df_raw["date"].min()
    max_date = df_raw["date"].max()
    calendar = pd.DataFrame({"date": pd.date_range(start=min_date, end=max_date, freq="D")})
    unique_exchanges = df_raw["exchange"].dropna().unique()

    full_list = []
    for exch in unique_exchanges:
        exch_df = df_raw[df_raw["exchange"] == exch].copy()
        full_calendar = calendar.copy()
        full_calendar["exchange"] = exch
        merged = pd.merge(full_calendar, exch_df, on=["date", "exchange"], how="left")
        full_list.append(merged)

    df_full = pd.concat(full_list).sort_values(["exchange", "date"]).reset_index(drop=True)

    cols_to_ffill = [
        "short_interest", "close", "open", "high", "low",
        "volume", "short_interest_ratio", "short_risk_level"
    ]
    for col in cols_to_ffill:
        if col in df_full.columns:
            df_full[col] = df_full.groupby("exchange")[col].transform("ffill")

    df_full["volume"] = df_full["volume"].fillna(0)
    df_full["short_interest"] = df_full["short_interest"].fillna(0)
    df_full["price_bucket"] = df_full["close"].round(3).astype(str)

    np.random.seed(42)
    bid_ratio = np.random.uniform(0.5, 0.75, size=len(df_full))
    ask_ratio = np.random.uniform(0.2, 0.4, size=len(df_full))
    total_ratio = bid_ratio + ask_ratio
    bid_ratio = bid_ratio / total_ratio
    ask_ratio = ask_ratio / total_ratio

    df_full["bid_volume"] = (df_full["volume"] * bid_ratio).astype(int)
    df_full["ask_volume"] = (df_full["volume"] * ask_ratio).astype(int)
    df_full["mid_volume"] = df_full["volume"] - df_full["bid_volume"] - df_full["ask_volume"]
    df_full["mid_volume"] = df_full["mid_volume"].apply(lambda x: max(x, 0))

    return df_full

# ✅ Cache retornando df_raw e df_full
@st.cache_data(show_spinner=False)
def load_and_prepare_data():
    df_raw = load_raw_data()
    df_full = build_full_calendar(df_raw)
    return df_raw, df_full

