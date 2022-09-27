def get_range(start=None, end=None, sheet_name=None):
    if not start and not end:
        _range = sheet_name
    elif not end:
        _range = f"{sheet_name}!{start}:Z"
    elif not start:
        _range = f"{sheet_name}!A:{end}"
    else:
        _range = f"{sheet_name}!{start}:{end}"

    return _range


def get_range_column_row(start, end=None, sheet_name=None):
    if not end:
        end = start
    _range = f'{sheet_name}!{start}:{end}'
    return _range


def get_range_colorize(row_start=None, row_end=None,
                       column_start=None, column_end=None, sheet_id=None):
    if not row_start and not row_end and not column_start and not column_end:
        return {"sheetId": sheet_id}
    _range = {'startRowIndex': row_start,
              'endRowIndex': row_end,
              'startColumnIndex': column_start,
              'endColumnIndex': column_end}
    if sheet_id:
        _range["sheetId"] = sheet_id
    return _range


def get_range_feedbacks(sheet_id, row=None):
    if not row:
        return {"sheetId": sheet_id}

    _range = {"sheetId": sheet_id,
              "startRowIndex": row,
              "endRowIndex": row + 1,
              "startColumnIndex": 6,
              "endColumnIndex": 10,
              }
    return _range
