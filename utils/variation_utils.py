def calculate_variation_arrow(current, previous):
    if previous == 0 or previous is None or current is None:
        return "—"

    if current == previous:
        return "<span style='color:#8e44ad;'>↔ 0.0%</span>"

    change = (current - previous) / previous
    percentage = abs(change * 100)

    if change > 0:
        return f"<span style='color:#27ae60;'>🔼 {percentage:.1f}%</span>"  # green
    else:
        return f"<span style='color:#c0392b;'>🔽 {percentage:.1f}%</span>"  # red
    
    