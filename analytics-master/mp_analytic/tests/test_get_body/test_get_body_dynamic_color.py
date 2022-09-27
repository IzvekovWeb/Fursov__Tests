import pytest

from data.google.get_body_methods.get_body import get_body_dynamic_color


def test_get_body_dynamic_color():
    body = {}
    expected_result = [[
        {
        "repeatCell": {
            "range": {
                "sheetId": 12345678,
                "startRowIndex": 0,
                "endRowIndex": 1
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0, "green": 0, "blue": 0},
                    "textFormat": {
                        "fontSize": 10,
                        "bold": True
                    }}},
            "fields": "userEnteredFormat(backgroundColor,textFormat)"
        }},
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": 12345678,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 12
                }}},
        {
            "updateCells": {
                "range": {
                    "sheetId": 12345678,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                },
                "rows": [{
                    "values": [{
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 255, "green": 255, "blue": 255}
                        }}]}],
                "fields": "userEnteredFormat.backgroundColor"
            }
        }
    ]]

    get_body_dynamic_color(
        body,
        sheet_id=12345678,
        color_headers={"red": 0, "green": 0, "blue": 0},
        start_row=0,
        end_row=1,
        start_col=0,
        end_col=1,
        color_cell={"red": 255, "green": 255, "blue": 255}
    )

    assert body['requests'] == expected_result


def test_get_body_dynamic_color_exceptions():
    body = {}

    with pytest.raises(TypeError):
        get_body_dynamic_color(
            body,
            sheet_id='12345678',
            color_headers={"red": 0, "green": 0, "blue": 0},
            start_row=0,
            end_row=1,
            start_col=0,
            end_col=1,
            color_cell={"red": 255, "green": 255, "blue": 255}
        )

        get_body_dynamic_color(
            body,
            sheet_id=12345678,
            color_headers={"red": 'text', "green": 'text', "blue": 'text'},
            start_row=0,
            end_row=1,
            start_col=0,
            end_col=1,
            color_cell={"red": 'text', "green": 'text', "blue": 'text'}
        )

        get_body_dynamic_color(
            body,
            sheet_id=12345678,
            color_headers=[0, 0, 0],
            start_row=0,
            end_row=1,
            start_col=0,
            end_col=1,
            color_cell=[255, 255, 255]
        )

    with pytest.raises(ValueError):
        get_body_dynamic_color(
            body,
            sheet_id=12345678,
            color_headers={"red": 0, "green": 0, "blue": 0},
            start_row=-1,
            end_row=-1,
            start_col=-1,
            end_col=-1,
            color_cell={"red": 255, "green": 255, "blue": 255}
        )

        get_body_dynamic_color(
            body,
            sheet_id=12345678,
            color_headers={"red": -1, "green": -1, "blue": 256},
            start_row=1,
            end_row=2,
            start_col=1,
            end_col=2,
            color_cell={"red": 300, "green": -12, "blue": 555}
        )
