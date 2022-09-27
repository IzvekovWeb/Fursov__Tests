from data.google.utils.decorators import check_instance


@check_instance
def get_body_create_spreadsheet(spreadsheet_title: str, sheet_title: str | int) -> dict:

    body = {
        'properties': {
            'title': spreadsheet_title, 'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'title': sheet_title,
                'gridProperties': {
                    'rowCount': 1000, 'columnCount': 26
                }}}]}
    return body


@check_instance
def get_body_add_sheet(sheet_title: str | int) -> dict:

    body = {
        "requests": [{
            "addSheet": {
                'properties': {
                    'sheetType': 'GRID',
                    'title': sheet_title,
                    'gridProperties': {
                        'rowCount': 1000, 'columnCount': 26
                    }}}}]}
    return body


@check_instance
def get_body_insert(_range: str, _values: list) -> dict:

    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": _range,
             "values": _values}
        ]}
    return body


@check_instance
def get_body_colorize(body: dict, _range: dict, _color: dict):

    if len(_range) == 0:
        raise ValueError

    if 'requests' not in body:
        body["requests"] = []

    body["requests"].append([{
        "repeatCell": {
            "range": _range,
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": _color
                },
            },
            "fields": "userEnteredFormat.backgroundColor"
        }}])


@check_instance
def get_body_conditional_color_format(
        sheet_id: str | int, start_row_index: str | int, end_row_index: str | int,
        min_color: dict, mid_color: dict, max_color: dict) -> dict:

    try:
        if int(sheet_id) < 0 or int(start_row_index) < 0 or int(end_row_index) < 0:
            raise ValueError
    except ValueError:
        raise

    body = {'requests': [{
        "addConditionalFormatRule": {
            "rule": {
                "ranges": [{
                    "sheetId": sheet_id,
                    "startRowIndex": start_row_index,
                    "endRowIndex": end_row_index
                }],
                "gradientRule": {
                    "minpoint": {
                        "color": min_color,
                        "type": "MIN"
                    },
                    "midpoint": {
                        "color": mid_color,
                        "type": "PERCENTILE",
                        "value": "50",
                    },
                    "maxpoint": {
                        "color": max_color,
                        "type": "MAX"
                    }}},
            "index": 0
        }}]}
    return body


@check_instance
def get_body_format(
        sheet_id: int | str = 0,
        start_row_index: int | str = 0,
        end_row_index: int | str = 0,
        start_column_index: int | str = 0,
        end_column_index: int | str = 0,
        number_type: str | None = None,
        number_pattern: str = '') -> dict:

    try:
        if (
            int(sheet_id) < 0 or
            int(start_row_index) < 0 or
            int(end_row_index) < 0 or
            int(start_column_index) < 0 or
            int(end_column_index) < 0
        ):
            raise ValueError
    except ValueError:
        raise

    number_types = ['TEXT', 'NUMBER', 'PERCENT', 'CURRENCY', 'DATE', 'TIME', 'DATE_TIME', 'SCIENTIFIC', 'NUMBER_FORMAT_TYPE_UNSPECIFIED']

    if number_type is None:
        number_type = 'NUMBER_FORMAT_TYPE_UNSPECIFIED'

    if number_type not in number_types:
        raise ValueError(f'Number type must be one of: {number_types}')

    body = {'requests': [{
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row_index,
                "endRowIndex": end_row_index,
                "startColumnIndex": start_column_index,
                "endColumnIndex": end_column_index
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {
                        "type": number_type,
                        "pattern": number_pattern
                    }}},
            "fields": "userEnteredFormat.numberFormat"
        }}]}
    return body


@check_instance
def get_body_clear_borders(sheet_id: int | str, border_style: dict) -> dict:

    try:
        if int(sheet_id) < 0:
            raise ValueError
    except ValueError:
        raise

    body = {
        "requests": [{
            "repeatCell": {
                'range': {
                    'sheetId': sheet_id
                },
                "cell": {
                    "userEnteredFormat": {
                        "borders":
                            {
                                'left': border_style,
                                'right': border_style,
                                'top': border_style,
                                'bottom': border_style
                            }}},
                "fields": "userEnteredFormat.borders"
            }}]}
    return body


@check_instance
def get_body_dynamic_color(
        body: dict,
        color_headers: dict,
        color_cell: dict,
        sheet_id: int | str = 0,
        start_row: int | str = 0,
        end_row: int | str = 0,
        start_col: int | str = 0,
        end_col: int | str = 0) -> None:

    try:
        if (
            int(sheet_id) < 0 or
            int(start_row) < 0 or
            int(end_row) < 0 or
            int(start_col) < 0 or
            int(end_col) < 0
        ):
            raise ValueError
    except ValueError:
        raise

    if 'requests' not in body:
        body["requests"] = []

    body["requests"].append([{
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": color_headers,
                    "textFormat": {
                        "fontSize": 10,
                        "bold": True
                    }}},
            "fields": "userEnteredFormat(backgroundColor,textFormat)"
        }},
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 12
                }}},
        {
            "updateCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": start_row,
                    "endRowIndex": end_row,
                    "startColumnIndex": start_col,
                    "endColumnIndex": end_col,
                },
                "rows": [{
                    "values": [{
                        "userEnteredFormat": {
                            "backgroundColor": color_cell
                        }}]}],
                "fields": "userEnteredFormat.backgroundColor"
            }}])


@check_instance
def get_body_clear_conditions(sheet_id: int | str) -> dict:

    try:
        if int(sheet_id) < 0:
            raise ValueError
    except ValueError:
        raise

    body = {
        "requests": [{
            "deleteConditionalFormatRule": {
                "index": 0,
                "sheetId": sheet_id
            }}]}
    return body


@check_instance
def get_body_feedbacks(body: dict, _range: dict, red: int = 25):

    if not (256 > red > 0):
        raise ValueError

    if 'requests' not in body:
        body["requests"] = []

    body["requests"].append([{
        "repeatCell": {
            "range": _range,
            "cell": {
                "userEnteredFormat": {
                    "textFormat": {
                        "foregroundColor": {
                            "red": red,
                            "green": 0,
                            "blue": 0},
                        "fontFamily": "Arial",
                        "bold": "true"
                    }}},
            "fields": "userEnteredFormat(textFormat)"
        }}])
