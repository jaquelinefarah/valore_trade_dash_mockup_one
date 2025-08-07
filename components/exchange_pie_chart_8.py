import streamlit as st
import altair as alt
import pandas as pd

def show_exchange_pie_chart_altair(df, period_label):
   
    # 1. Filtrar dados reais
    df = df[df["volume"] > 0].copy()

    # 2. Agrupar e calcular %
    exchange_counts = df["exchange"].value_counts().rename_axis("exchange").reset_index(name="num_trades")
    total = exchange_counts["num_trades"].sum()
    exchange_counts["percent"] = (exchange_counts["num_trades"] / total) * 100
    exchange_counts["label"] = exchange_counts.apply(lambda row: f"{row['exchange']} ({row['percent']:.1f}%)", axis=1)

    # 3. Base chart
    base = alt.Chart(exchange_counts).encode(
        theta=alt.Theta("num_trades:Q", stack=True),
        color=alt.Color(
            "exchange:N",
            title="Exchange",
            legend=alt.Legend(
                labelFontSize=14,
                titleFontSize=16
            )
        )
    )

    pie = base.mark_arc(innerRadius=60, outerRadius=120)

    text = base.mark_text(radius=140, size=18, fontWeight="bold").encode(
        text=alt.Text("label:N"),
        color=alt.value("black")
    )

    # 4. Render
    st.markdown(f"**Exchange Distribution – {period_label}**")
    st.markdown(f"**Total Trades:** {total:,}")
    st.altair_chart(pie + text, use_container_width=True)
