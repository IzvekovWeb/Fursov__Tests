def border_constructor(style: str, width: int | str,  color: dict) -> dict:

    border_styles = ['DOTTED', 'DASHED', 'SOLID', 'SOLID_MEDIUM', 'SOLID_THICK', 'NONE', 'DOUBLE']

    if style is None or style == '':
        style = 'NONE'

    if not (isinstance(style, str) and isinstance(width, (int, str)) and isinstance(color, dict)):
        raise TypeError

    try:
        if int(width) < 0:
            raise ValueError
    except TypeError:
        raise TypeError

    if style not in border_styles:
        raise ValueError

    return {
        "style": style,
        "width": width,
        "color": color,
    }
