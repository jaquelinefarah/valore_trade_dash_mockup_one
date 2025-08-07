import pandas as pd

def get_last_closed_week(df_full):
    # Ensure the 'date' column is in datetime format
    df_full["date"] = pd.to_datetime(df_full["date"])

    # Identify the last available business day (Monday–Friday) in the dataset
    last_date = df_full["date"].max()

    # Get the last 5 business days up to and including last_date
    last_week_days = pd.bdate_range(end=last_date, periods=5)

    # Define start and end of the last full business week
    start_week = last_week_days[0]
    end_week = last_week_days[-1]

    # Create a label for display (e.g., "Jul 22 – 26, 2025")
    label = f"{start_week.strftime('%b %d')} – {end_week.strftime('%d, %Y')}"

    # Filter the DataFrame to include only the 5 business days of the week
    df_filtered = df_full[df_full["date"].isin(last_week_days)].copy()

    return df_filtered, label, start_week, end_week

