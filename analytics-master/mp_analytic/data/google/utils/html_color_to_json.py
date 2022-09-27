def html_color_to_json(html_color: str) -> dict:
    if html_color.startswith("#"):
        html_color = html_color[1:]
    return {"red": int(html_color[0:2], 16) / 255.0, "green": int(html_color[2:4], 16) / 255.0,
            "blue": int(html_color[4:6], 16) / 255.0}
