def get_body_create_spreadsheet(spreadsheet_title, sheet_title):
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


def get_body_add_sheet(sheet_title):
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


def get_body_insert(_range, _values):
    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": _range,
             "values": _values}
        ]}
    return body


def get_body_colorize(body, _range, _color):
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


def get_body_conditional_color_format(*args):
    body = {'requests': [{
        "addConditionalFormatRule": {
            "rule": {
                "ranges": [{
                    "sheetId": args[0],
                    "startRowIndex": args[1],
                    "endRowIndex": args[2]
                }],
                "gradientRule": {
                    "minpoint": {
                        "color": args[3],
                        "type": "MIN"
                    },
                    "midpoint": {
                        "color": args[4],
                        "type": "PERCENTILE",
                        "value": "50",
                    },
                    "maxpoint": {
                        "color": args[5],
                        "type": "MAX"
                    }}},
            "index": 0
        }}]}
    return body


def get_body_format(*args):
    body = {'requests': [{
        "repeatCell": {
            "range": {
                "sheetId": args[0],
                "startRowIndex": args[1],
                "endRowIndex": args[2],
                "startColumnIndex": args[3],
                "endColumnIndex": args[4]
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {
                        "type": args[5],
                        "pattern": args[6]
                    }}},
            "fields": "userEnteredFormat.numberFormat"
        }}]}
    return body


def get_body_clear_borders(sheet_id, constructor):
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
                                'left': constructor,
                                'right': constructor,
                                'top': constructor,
                                'bottom': constructor
                            }}},
                "fields": "userEnteredFormat.borders"
            }}]}
    return body


def get_body_dynamic_color(body, **kwargs):
    body["requests"].append([{
        "repeatCell": {
            "range": {
                "sheetId": kwargs['sheet_id'],
                "startRowIndex": 0,
                "endRowIndex": 1
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": kwargs['color_headers'],
                    "textFormat": {
                        "fontSize": 10,
                        "bold": True
                    }}},
            "fields": "userEnteredFormat(backgroundColor,textFormat)"
        }},
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": kwargs['sheet_id'],
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 12
                }}},
        {
            "updateCells": {
                "range": {
                    "sheetId": kwargs['sheet_id'],
                    "startRowIndex": kwargs['start_row'],
                    "endRowIndex": kwargs['end_row'],
                    "startColumnIndex": kwargs['start_col'],
                    "endColumnIndex": kwargs['end_col'],
                },
                "rows": [{
                    "values": [{
                        "userEnteredFormat": {
                            "backgroundColor": kwargs['color_cell']
                        }}]}],
                "fields": "userEnteredFormat.backgroundColor"
            }}])


def get_body_clear_conditions(sheet_id):
    body = {
        "requests": [{
            "deleteConditionalFormatRule": {
                "index": 0,
                "sheetId": sheet_id
            }}]}
    return body


def get_body_feedbacks(body, _range, red=25):
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
