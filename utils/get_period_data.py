import pandas as pd

def get_period_data(df_filtered, period_label, start_week, end_week, business_day=5):
    df = df_filtered.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Período atual
    period_end = end_week
    period_start = pd.bdate_range(end=period_end, periods=business_day)[0]
    current_df = df[(df["date"] >= period_start) & (df["date"] <= period_end)]

    # Período anterior
    prev_end = period_start - pd.Timedelta(days=1)
    prev_start = pd.bdate_range(end=prev_end, periods=business_day)[0]
    previous_df = df[(df["date"] >= prev_start) & (df["date"] <= prev_end)]

    return current_df.copy(), previous_df.copy()
