import streamlit as st 
import plotly.graph_objects as go
import pandas as pd

def show_candlestick_chart_plotly(df_full, start_date, end_date, period_label="Selected Period"):
    # Garantir formato e ordenação da data
    df = df_full[df_full["close"].notna()].copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.sort_values("date")

    # Filtrar período
    df_filtered = df[(df["date"] >= start_date.date()) & (df["date"] <= end_date.date())]

    # Agregar por dia
    df_daily = df_filtered.groupby("date").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last"
    }).reset_index()

    # Criar gráfico
    fig = go.Figure()

    # Candlestick principal (sem legenda automática)
    fig.add_trace(go.Candlestick(
        x=df_daily['date'],
        open=df_daily['open'],
        high=df_daily['high'],
        low=df_daily['low'],
        close=df_daily['close'],
        increasing_line_color='green',
        decreasing_line_color='red',
        showlegend=False
    ))

    # Legenda customizada com traços invisíveis
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(size=10, color='green', symbol='square'),
        name='Price Up (Open < Close)'
    ))
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(size=10, color='red', symbol='square'),
        name='Price Down (Open > Close)'
    ))

    # Layout com legenda
    fig.update_layout(
        title=f"Open & Close Price Candlestick – {period_label}",
        xaxis_title="Date",
        yaxis_title="Price ($ CAD)",
        xaxis_rangeslider_visible=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        )
    )

    st.plotly_chart(fig, use_container_width=True)