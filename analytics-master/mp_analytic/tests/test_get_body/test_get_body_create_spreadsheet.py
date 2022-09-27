import pytest

from data.google.get_body_methods.get_body import get_body_create_spreadsheet

expected_result_1 = {
    'properties': {
        'title': 'Test_1', 'locale': 'ru_RU'
    },
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'title': 'Test_1_Sheet_1',
            'gridProperties': {
                'rowCount': 1000, 'columnCount': 26
            }}}]}
expected_result_2 = {
    'properties': {
        'title': 1, 'locale': 'ru_RU'
    },
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'title': 2,
            'gridProperties': {
                'rowCount': 1000, 'columnCount': 26
            }}}]}
expected_result_3 = {
    'properties': {
        'title': '', 'locale': 'ru_RU'
    },
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'title': '',
            'gridProperties': {
                'rowCount': 1000, 'columnCount': 26
            }}}]}


def test_get_body_create_spreadsheet():

    assert get_body_create_spreadsheet('Test_1', 'Test_1_Sheet_1') == expected_result_1
    assert get_body_create_spreadsheet('', '') == expected_result_3


def test_get_body_create_spreadsheet_exceptions():

    with pytest.raises(TypeError):
        get_body_create_spreadsheet([], [])
    with pytest.raises(TypeError):
        get_body_create_spreadsheet('Title', {})
    with pytest.raises(TypeError):
        get_body_create_spreadsheet({}, 'Title')
    with pytest.raises(TypeError):
        get_body_create_spreadsheet(1, 2)
