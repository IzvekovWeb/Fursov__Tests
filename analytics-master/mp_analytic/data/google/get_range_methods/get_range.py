from data.google.utils.decorators import check_instance


@check_instance
def get_range(start: int | str | None = None,
              end: int | str | None = None,
              sheet_name: int | str | None = None) -> str:

    if sheet_name is None:
        sheet_name = ""
    elif start or end:
        sheet_name = f"'{sheet_name}'"

    if not start and not end:
        if not sheet_name:
            return "A:Z"
        _range = sheet_name
    elif not end:
        _range = f"{sheet_name}!{start}:Z"
    elif not start:
        _range = f"{sheet_name}!A:{end}"
    else:
        _range = f"{sheet_name}!{start}:{end}"

    return _range


@check_instance
def get_range_column_row(
        start: int | str | None = None,
        end: int | str | None = None,
        sheet_name: int | str | None = None) -> str:

    if isinstance(end, str):
        end.replace('-', '')

    if sheet_name is None:
        sheet_name = ""
    elif start or end:
        sheet_name = f"'{sheet_name}'"

    if start is None:
        start = '1'

    if not end:
        end = start
    _range = f"{sheet_name}!{start}:{end}"
    return _range


@check_instance
def get_range_colorize(row_start: int | None = None, row_end: int | None = None,
                       column_start: int | None = None, column_end: int | None = None,
                       sheet_id: int | str | None = None) -> dict:

    if (row_end is not None and row_end < 0) or (column_end is not None and column_end < 0):
        raise ValueError('Row and Column end must be non negative')

    if not row_start and not row_end and not column_start and not column_end:
        return {"sheetId": sheet_id}

    _range = {'startRowIndex': row_start,
              'endRowIndex': row_end,
              'startColumnIndex': column_start,
              'endColumnIndex': column_end}
    if sheet_id:
        _range["sheetId"] = sheet_id
    return _range


@check_instance
def get_range_feedbacks(sheet_id: int, row: int | None = None) -> dict:

    if row is not None and row < 0:
        raise ValueError

    if not row:
        return {"sheetId": sheet_id}

    _range = {"sheetId": sheet_id,
              "startRowIndex": row,
              "endRowIndex": row + 1,
              "startColumnIndex": 6,
              "endColumnIndex": 10,
              }
    return _range
