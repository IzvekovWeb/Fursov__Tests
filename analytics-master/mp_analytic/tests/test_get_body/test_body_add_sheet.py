import pytest

from data.google.get_body_methods.get_body import get_body_add_sheet


def test_get_body_add_sheet():

    expected_result_1 = {
        "requests": [{
            "addSheet": {
                'properties': {
                    'sheetType': 'GRID',
                    'title': 'Title_1',
                    'gridProperties': {
                        'rowCount': 1000, 'columnCount': 26
                    }
                }
            }
        }]
    }
    expected_result_2 = {
        "requests": [{
            "addSheet": {
                'properties': {
                    'sheetType': 'GRID',
                    'title': '',
                    'gridProperties': {
                        'rowCount': 1000, 'columnCount': 26
                    }}}}]}

    assert get_body_add_sheet('Title_1') == expected_result_1
    assert get_body_add_sheet('') == expected_result_2


def test_get_body_add_sheet_exceptions():
    with pytest.raises(TypeError):
        get_body_add_sheet({'Title'})

    with pytest.raises(TypeError):
        get_body_add_sheet(['Title'])

    with pytest.raises(TypeError):
        get_body_add_sheet({1: 'Title'})
