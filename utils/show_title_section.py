def get_section_title_html(title: str, period_label: str, comparison_label: str) -> str:
    return f"""
    <div style='text-align: center; margin-top: 10px; margin-bottom: 25px;'>
        <h2 style='margin-bottom: 5px;'>{title}</h2>
        <p style='color: gray; font-size: 0.9em;'>
            <b>Reference Period:</b> {period_label}<br>
            Compared to the <b>{comparison_label}</b>
        </p>
    </div>
    """