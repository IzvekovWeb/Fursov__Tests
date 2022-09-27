from application.errors.google import NotCorrectInputValuesException
from config.color_constants import GRAY
from data.google.get_body_methods.get_body import get_body_clear_borders
from data.google.utils.constructors import border_constructor


def update_borders(sheet_id, start_row, end_row,
                   start_column, end_column,
                   left, right, bottom, top,
                   width, style, color, clear):
    if clear:
        return get_body_clear_borders(sheet_id, border_constructor('SOLID', width, GRAY))

    if not start_row and not end_row and not start_column and not end_column:
        range_ = {"sheetId": sheet_id,
                  'startRowIndex': 0,
                  'endRowIndex': 10000,
                  'startColumnIndex': 0,
                  'endColumnIndex': 30}
    else:
        range_ = {"sheetId": sheet_id}

        if start_row and end_row:
            if start_row > end_row:
                raise NotCorrectInputValuesException("Неверно заданы границы")
            else:
                range_['startRowIndex'] = start_row
                range_['endRowIndex'] = end_row

        elif start_row:
            range_['startRowIndex'] = start_row
            range_['endRowIndex'] = 10000
        elif end_row:
            range_['startRowIndex'] = 0
            range_['endRowIndex'] = end_row
        else:
            range_['startRowIndex'] = 0
            range_['endRowIndex'] = 10000

        if start_column and end_column:
            if start_column > end_column:
                raise NotCorrectInputValuesException("Неверно заданы границы")
            else:
                range_['startColumnIndex'] = start_column
                range_['endColumnIndex'] = end_column
        elif start_column:
            range_['startColumnIndex'] = start_column
            range_['endColumnIndex'] = start_column + 30
        elif end_column:
            range_['startColumnIndex'] = 0
            range_['endColumnIndex'] = end_column
        else:
            range_['startColumnIndex'] = 0
            range_['endColumnIndex'] = 30

    request = {
        "updateBorders": {
            "range": range_}}

    if left:
        request['updateBorders']['left'] = border_constructor(style, width, color)
    if right:
        request['updateBorders']['right'] = border_constructor(style, width, color)
    if bottom:
        request['updateBorders']['bottom'] = border_constructor(style, width, color)
    if top:
        request['updateBorders']['top'] = border_constructor(style, width, color)

    body = {
        "requests": [
            request]}
    return body
