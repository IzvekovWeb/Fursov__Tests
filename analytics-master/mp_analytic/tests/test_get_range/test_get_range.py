import pytest

from data.google.get_range_methods.get_range import get_range


def test_get_range():
    assert get_range(sheet_name='Мой лист') == 'Мой лист'
    assert get_range(start=1, sheet_name='Мой лист') == "'Мой лист'!1:Z"
    assert get_range(start=1, end=5, sheet_name='Мой лист') == "'Мой лист'!1:5"
    assert get_range(start=None, end=5, sheet_name=None) == "!A:5"
    assert get_range(start=4, end=None, sheet_name=None) == "!4:Z"
    assert get_range(start=None, end=None, sheet_name=None) == "A:Z"
    assert get_range('A1', 6, 'Мой лист') == "'Мой лист'!A1:6"
    assert get_range('A1', '', 'Мой лист') == "'Мой лист'!A1:Z"
    assert get_range('', 111, 'Мой лист') == "'Мой лист'!A:111"
    assert get_range(1, 2, 555) == "'555'!1:2"
    assert get_range(start='A1', end='C') == "!A1:C"
    assert get_range() == "A:Z"


def test_get_range_exceptions():
    with pytest.raises(TypeError):
        get_range([123], 1, '1')
    with pytest.raises(TypeError):
        get_range(1, {123}, '1')
    with pytest.raises(TypeError):
        get_range(1, 2, ('List', ))
