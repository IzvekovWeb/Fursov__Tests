import pytest

from data.google.get_body_methods.get_body import get_body_feedbacks


def test_get_body_feedbacks():
    body = {}
    expected_result = [[
        {
            "repeatCell": {
                "range": {
                      "sheetId": 1427492153,
                      "startRowIndex": 0,
                      "endRowIndex": 1,
                      "startColumnIndex": 0,
                      "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "foregroundColor": {
                                "red": 111,
                                "green": 0,
                                "blue": 0},
                            "fontFamily": "Arial",
                            "bold": "true"
                        }}},
                "fields": "userEnteredFormat(textFormat)"
            }}
    ]]

    get_body_feedbacks(
        body,
        {
           "sheetId": 1427492153,
           "startRowIndex": 0,
           "endRowIndex": 1,
           "startColumnIndex": 0,
           "endColumnIndex": 1
        },
        111
    )

    assert body['requests'] == expected_result

    body = {}
    expected_result_2 = [[
        {
            "repeatCell": {
                "range": {
                    "sheetId": 1427492153,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "foregroundColor": {
                                "red": 25,
                                "green": 0,
                                "blue": 0},
                            "fontFamily": "Arial",
                            "bold": "true"
                        }}},
                "fields": "userEnteredFormat(textFormat)"
            }}
    ]]

    get_body_feedbacks(
        body,
        {
            "sheetId": 1427492153,
            "startRowIndex": 0,
            "endRowIndex": 1,
            "startColumnIndex": 0,
            "endColumnIndex": 1
        }
    )

    assert body['requests'] == expected_result_2


def test_get_body_feedbacks_exceptions():
    with pytest.raises(TypeError):
        body = {}
        get_body_feedbacks(body, {}, '111')

    with pytest.raises(TypeError):
        body = {}
        get_body_feedbacks(body, [], 111)

    with pytest.raises(ValueError):
        body = {}
        get_body_feedbacks(body, {}, -1)
        get_body_feedbacks(body, {}, 299)
        get_body_feedbacks(body, {
           "sheetId": -1427492153,
           "startRowIndex": 0,
           "endRowIndex": 1,
           "startColumnIndex": 0,
           "endColumnIndex": 1
        }, 0)
