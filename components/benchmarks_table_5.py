import streamlit as st
import pandas as pd
from utils.variation_utils import calculate_variation_arrow
from utils.get_period_data import get_period_data
from components.get_last_closed_week_2 import get_last_closed_week

# Mapeamento de dias úteis por label
DAYS_MAP = {
    "% Week": 5,
    "% Month": 21,
    "% Quarter": 63,
    "% Year": 252
}

def format_val(val):
    return f"${val:.4f}" if pd.notna(val) else "—"

def show_benchmarks_table(df_full):
    
    # === Obter a última semana fechada ===
    df_filtered, period_label, start_week, end_week = get_last_closed_week(df_full.copy())

    # === Inicializar estrutura de resultados ===
    table_data = {
        "Current Price": {"Last Closed Week": "—"},
        "VWAP": {"Last Closed Week": "—"},
        "TWAP": {"Last Closed Week": "—"}
    }

    # === Calcular valor atual da última semana ===
    current_df = df_filtered.copy()
    if not current_df.empty:
        table_data["Current Price"]["Last Closed Week"] = format_val(current_df["close"].ffill().iloc[-1])
        table_data["VWAP"]["Last Closed Week"] = format_val((current_df["close"] * current_df["volume"]).sum() / current_df["volume"].sum())
        table_data["TWAP"]["Last Closed Week"] = format_val(current_df["close"].mean())

    # === Para cada período, calcular a variação ===
    for label, business_day in DAYS_MAP.items():
        current_df, previous_df = get_period_data(
            df_filtered=df_full.copy(),
            period_label=label,
            start_week=end_week,
            end_week=end_week,
            business_day=business_day
        )

        if current_df.empty or previous_df.empty:
            table_data["Current Price"][label] = "—"
            table_data["VWAP"][label] = "—"
            table_data["TWAP"][label] = "—"
            continue

        # Cálculo atual
        current_price = current_df["close"].ffill().iloc[-1]
        current_vwap = (current_df["close"] * current_df["volume"]).sum() / current_df["volume"].sum()
        current_twap = current_df["close"].mean()

        # Cálculo anterior
        prev_price = previous_df["close"].ffill().iloc[-1]
        prev_vwap = (previous_df["close"] * previous_df["volume"]).sum() / previous_df["volume"].sum()
        prev_twap = previous_df["close"].mean()

        # Variações
        table_data["Current Price"][label] = calculate_variation_arrow(current_price, prev_price)
        table_data["VWAP"][label] = calculate_variation_arrow(current_vwap, prev_vwap)
        table_data["TWAP"][label] = calculate_variation_arrow(current_twap, prev_twap)

    # === Converter para DataFrame e exibir ===
    df_benchmarks = pd.DataFrame(table_data).T  # Transpor para ter métricas como linhas
    df_benchmarks.columns.name = None
    st.markdown(df_benchmarks.to_html(escape=False, index=True), unsafe_allow_html=True)
