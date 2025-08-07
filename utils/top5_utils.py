import plotly.express as px
import pandas as pd
import streamlit as st

def get_top5_consolidated_df(filtered_df):
    # Filtra nulos e calcula volume real transacionado
    df = filtered_df[filtered_df["price_bucket"].notna()].copy()
    df["price_bucket"] = df["price_bucket"].astype(float)
    df["volume"] = df[["bid_volume", "ask_volume"]].min(axis=1)

    # Identifica os 5 buckets com maior volume
    top_buckets = (
        df.groupby("price_bucket")["volume"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .index.tolist()
    )

    # Filtra apenas os top 5 e ordena visualmente
    df_top5 = df[df["price_bucket"].isin(top_buckets)].copy()
    df_top5 = df_top5.sort_values("price_bucket")

    # Cria coluna categórica ordenada com nome claro
    ordered_categories = [f"{x:.3f}" for x in df_top5["price_bucket"].unique()]
    df_top5["category_price_bucket"] = pd.Categorical(
        [f"{x:.3f}" for x in df_top5["price_bucket"]],
        categories=ordered_categories,
        ordered=True
    )

    # === Consolida ===
    df_consolidated = (
        df_top5.groupby("category_price_bucket")[["bid_volume", "ask_volume"]]
        .sum()
        .reset_index()
    )

    df_consolidated["total_volume"] = df_consolidated["bid_volume"] + df_consolidated["ask_volume"]

    return df_consolidated
