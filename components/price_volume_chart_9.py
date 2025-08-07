import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_price_volume_chart_plotly(df_full, start_date, end_date, period_label="Selected Period"):
   
    # 1. Preparar dados
    df_clean = df_full[df_full["close"].notna()].copy()
    grouped = df_clean.groupby("date").agg({
        "close": "mean",
        "volume": "sum"
    }).reset_index()
    grouped["SMA_15"] = grouped["close"].rolling(window=15, min_periods=1).mean()

    # 2. Aplicar filtro de período externo
    filtered = grouped[grouped["date"].between(start_date, end_date)].copy()

    # 3. Criar figura Plotly
    fig = go.Figure()

    # Volume em barras
    fig.add_trace(go.Bar(
        x=filtered["date"],
        y=filtered["volume"],
        name="Volume (Shares)",
        marker_color="orange",
        yaxis="y2",
        opacity=0.5
    ))

    # Preço médio
    fig.add_trace(go.Scatter(
        x=filtered["date"],
        y=filtered["close"],
        name="Avg. Price ($ CAD)",
        mode="lines+markers",
        line=dict(color="royalblue"),
        connectgaps=True
    ))

    # Média móvel
    fig.add_trace(go.Scatter(
        x=filtered["date"],
        y=filtered["SMA_15"],
        name="15-Day SMA",
        mode="lines",
        line=dict(color="green", dash="dot"),
        connectgaps=True
    ))

    # Layout
    fig.update_layout(
    title=f"Price & Volume – {period_label}",
    height=500,
    legend=dict(
        orientation="h",
        y=-0.2,
        font=dict(size=18)  # ← aumenta o tamanho da legenda
    ),
    margin=dict(t=50, b=100),
    xaxis=dict(title="Date"),
    yaxis=dict(title="Avg. Price ($ CAD)", side="left"),
    yaxis2=dict(
        title="Volume (Shares)",
        overlaying="y",
        side="right",
        showgrid=False
    )
)

    st.plotly_chart(fig, use_container_width=True)
