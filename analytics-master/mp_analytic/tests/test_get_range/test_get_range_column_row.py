import pytest

from data.google.get_range_methods.get_range import get_range_column_row


def test_get_range_column_row():
    assert get_range_column_row('A1', 2) == "!A1:2"
    assert get_range_column_row('1', 'A2') == "!1:A2"
    assert get_range_column_row('A1', 'C3', 'Мой лист') == "'Мой лист'!A1:C3"
    assert get_range_column_row('A1', 3, 'List') == "'List'!A1:3"
    assert get_range_column_row(-3, 4) == "!-3:4"
    assert get_range_column_row() == "!1:1"
    assert get_range_column_row(start=1, end=None, sheet_name=None) == "!1:1"
    assert get_range_column_row(start=None, end=2, sheet_name=None) == "!1:2"
    assert get_range_column_row(start=2, end=2, sheet_name=None) == "!2:2"
    assert get_range_column_row(start=1, end=3, sheet_name='AAA') == "'AAA'!1:3"


def test_get_range_column_row_exceptions():

    with pytest.raises(TypeError):
        get_range_column_row([])
        get_range_column_row('A1', {})
        get_range_column_row('A1', 'C1', ('List', ))
