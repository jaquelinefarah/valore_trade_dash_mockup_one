def format_variation_for_metric(current, previous):
    if previous is None or previous == 0 or current is None:
        return None, "↔", "gray"

    change = current - previous
    percentage = (change / previous) * 100

    if abs(percentage) < 0.1:
        return "0.0%", "↔", "gray"
    elif percentage > 0:
        return f"{percentage:.1f}%", "", "#27ae60"
    else:
        return f"{abs(percentage):.1f}%", "", "#c0392b"
