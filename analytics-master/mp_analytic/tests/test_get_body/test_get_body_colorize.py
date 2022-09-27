import pytest

from data.google.get_body_methods.get_body import get_body_colorize


def test_get_body_colorize():
    body = {}
    _range = {
        "sheetId": 0,
        "startRowIndex": 0,
        "endRowIndex": 3,
        "startColumnIndex": 0,
        "endColumnIndex": 5,
    }
    _color = {
        "red": 0,
        "green": 0,
        "blue": 0
    }
    expected_result_1 = [[{
        "repeatCell": {
            "range": {
                "sheetId": 0,
                "startRowIndex": 0,
                "endRowIndex": 3,
                "startColumnIndex": 0,
                "endColumnIndex": 5,
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    },
                },
            },
            "fields": "userEnteredFormat.backgroundColor"
        }}]]
    expected_result_2 = [[{
        "repeatCell": {
            "range": {
                "sheetId": 0,
                "startRowIndex": 0,
                "endRowIndex": 3
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    },
                },
            },
            "fields": "userEnteredFormat.backgroundColor"
        }}]]

    get_body_colorize(body, _range, _color)
    assert body['requests'] == expected_result_1

    _range2 = {
        "sheetId": 0,
        "startRowIndex": 0,
        "endRowIndex": 3
    }
    body = {}
    get_body_colorize(body, _range2, _color)
    assert body['requests'] == expected_result_2

    body = {}
    get_body_colorize(body, _range, _color)
    assert body['requests'] == expected_result_1


def test_get_body_colorize_exceptions():
    _range = {
        "sheetId": 0,
        "startRowIndex": 0,
        "endRowIndex": 3,
        "startColumnIndex": 0,
        "endColumnIndex": 5,
    }
    _color = {
        "red": 0,
        "green": 0,
        "blue": 0
    }

    # Проверки _range
    body = {}
    with pytest.raises(TypeError):
        get_body_colorize(body, 'Лист1!A1:E4', _color)

    body = {}
    with pytest.raises(TypeError):
        get_body_colorize(body, 'A1:E4', _color)

    with pytest.raises(TypeError):
        get_body_colorize(body, ['Лист1', 'A1', 'E4'], _color)

    with pytest.raises(ValueError):
        _range = {}
        get_body_colorize(body, _range, _color)

    # Проверки _color
    body = {}
    with pytest.raises(TypeError):
        get_body_colorize(body, _range, [0, 0, 0])

    body = {}
    with pytest.raises(TypeError):
        get_body_colorize(body, _range, (0, 0, 0))

    body = {}
    with pytest.raises(TypeError):
        get_body_colorize(body, _range, "0, 0, 0")
