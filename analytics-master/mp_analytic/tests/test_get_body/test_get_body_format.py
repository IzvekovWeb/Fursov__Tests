import pytest

from data.google.get_body_methods.get_body import get_body_format


def test_get_body_format():
    expected_result_1 = {'requests': [{
        "repeatCell": {
            "range": {
                "sheetId": 0,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": 1
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {
                        "type": "TEXT",
                        "pattern": ""
                    }}},
            "fields": "userEnteredFormat.numberFormat"
        }}]}
    assert get_body_format(
        0,
        0, 1,
        0, 1,
        'TEXT',
        ''
        ) == expected_result_1

    expected_result_2 = {'requests': [{
        "repeatCell": {
            "range": {
                "sheetId": 12345678,
                "startRowIndex": 4,
                "endRowIndex": 10,
                "startColumnIndex": 5,
                "endColumnIndex": 11
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {
                        "type": "NUMBER",
                        "pattern": ""
                    }}},
            "fields": "userEnteredFormat.numberFormat"
        }}]}
    assert get_body_format(
        12345678,
        4, 10,
        5, 11,
        'NUMBER',
        ''
        ) == expected_result_2


def test_get_body_format_exceptions():
    with pytest.raises(TypeError):
        get_body_format(
            [],
            {}, '1',
            5, 11,
            'NUMBER',
            ''
        )

    with pytest.raises(ValueError):
        get_body_format(
            12345678,
            4, 10,
            5, 11,
            'CHISLO',
            ''
        )