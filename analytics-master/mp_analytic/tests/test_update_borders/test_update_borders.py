import pytest

from data.google.update_cells.update_borders import update_borders, NotCorrectInputValuesException
from expected_rezults import *


def fake_get_body_clear_borders(sheet_id, constructor):
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
                                "left": constructor,
                                "right": constructor,
                                "top": constructor,
                                "bottom": constructor
                            }}},
                "fields": "userEnteredFormat.borders"
            }}]}
    return body


def fake_border_constructor(color=None):
    def a(style, width, color_):
        return{
            'style': style,
            'width': width,
            'color': color
        }
    return a


def fake_html_color_to_json(r, g, b):
    return {"red": r, "green": g, "blue": b}


def test_update_borders(monkeypatch):
    path = 'data.google.update_cells.update_borders.get_body_clear_borders'

    monkeypatch.setattr('data.google.update_cells.update_borders.border_constructor',
                        fake_border_constructor({"red": 0, "green": 0, "blue": 0}))
    monkeypatch.setattr(path, fake_get_body_clear_borders)

    # Clear True
    result = update_borders(
        12345678, 0, 10000, 0, 30,
        True, True, True, True,
        1, "SOLID", {"red": 0, "green": 0, "blue": 0}, True
    )
    assert expected_clear_true == result

    # Without starts and ends
    result = update_borders(
        12345678, None, '', '', None,
        True, True, True, True,
        2, "SOLID", {"red": 0, "green": 0, "blue": 0}, False
    )
    assert expected_without_starts_ends == result

    # Rows and columns
    result = update_borders(
        12345678, 0, 10000, 0, 30,
        True, True, True, True,
        2, "SOLID", {"red": 0, "green": 0, "blue": 0}, False
    )
    assert expected_rows_and_columns == result

    # Rows only
    result = update_borders(
        12345678, 1, 5, None, None,
        True, True, True, True,
        2, "SOLID", {"red": 0, "green": 0, "blue": 0}, False
    )
    assert expected_rows_only == result

    # start_row_and_column_only
    result = update_borders(
        12345678, 1, None, 2, None,
        True, True, True, True,
        2, "SOLID", {"red": 0, "green": 0, "blue": 0}, False
    )
    assert expected_start_row_and_column_only == result

    # end_row_and_column_only
    result = update_borders(
        12345678, None, 3, None, 5,
        True, True, True, True,
        2, "SOLID", {"red": 0, "green": 0, "blue": 0}, False
    )
    assert expected_end_row_and_column_only == result

    # columns_only
    result = update_borders(
        12345678, None, None, 2, 6,
        True, True, True, True,
        2, "SOLID", {"red": 0, "green": 0, "blue": 0}, False
    )
    assert expected_columns_only == result

    # Top Only
    result = update_borders(
        12345678, None, '', '', None,
        False, False, False, True,
        2, "SOLID", {"red": 0, "green": 0, "blue": 0}, False
    )
    assert expected_top_only == result


def test_update_borders_exceptions_value(monkeypatch):
    path = 'data.google.update_cells.update_borders.get_body_clear_borders'

    monkeypatch.setattr('data.google.update_cells.update_borders.border_constructor',
                        fake_border_constructor({"red": 0, "green": 0, "blue": 0}))
    monkeypatch.setattr(path, fake_get_body_clear_borders)

    with pytest.raises(NotCorrectInputValuesException):
        update_borders(
            12345678, 1, 2, 100, 30,
            True, True, True, True,
            1, "SOLID", {"red": 0, "green": 0, "blue": 0}, False
        )

    with pytest.raises(NotCorrectInputValuesException):
        update_borders(
            12345678, 10, 1, 0, 30,
            True, True, True, True,
            1, "SOLID", {"red": 0, "green": 0, "blue": 0}, False
        )

    with pytest.raises(NotCorrectInputValuesException):
        update_borders(
            12345678, 10, 1, 0, 30,
            True, True, True, True,
            1, "SOME NOT COOL VALUE", {"red": 0, "green": 0, "blue": 0}, False
        )

    with pytest.raises(NotCorrectInputValuesException):
        update_borders(
            12345678, 10, 1, 0, 30,
            True, True, True, True,
            -10, "DASHED", {"red": 0, "green": 0, "blue": 0}, False
        )


def test_update_borders_exceptions_type(monkeypatch):
    path = 'data.google.update_cells.update_borders.get_body_clear_borders'

    monkeypatch.setattr('data.google.update_cells.update_borders.border_constructor',
                        fake_border_constructor({"red": 0, "green": 0, "blue": 0}))
    monkeypatch.setattr(path, fake_get_body_clear_borders)

    with pytest.raises(TypeError):
        update_borders(
            12345678, [], {}, (1, ), {'colEnd': 1},
            True, True, True, True,
            1, "SOLID", {"red": 0, "green": 0, "blue": 0}, False
        )

    with pytest.raises(NotCorrectInputValuesException):
        update_borders(
            12345678, 10, 1, 0, 30,
            True, True, True, True,
            1, "SOLID", [], False
        )

    with pytest.raises(NotCorrectInputValuesException):
        update_borders(
            12345678, 10, 1, 0, 30,
            True, True, True, True,
            1, "SOLID", "red", False
        )
