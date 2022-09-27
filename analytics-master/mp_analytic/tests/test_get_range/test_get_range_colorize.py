import pytest

from data.google.get_range_methods.get_range import get_range_colorize


def test_get_range_colorize():
    expected = {
        'sheetId': 123456789,
        'startRowIndex': 1,
        'endRowIndex': 2,
        'startColumnIndex': 1,
        'endColumnIndex': 2
    }
    expected_2 = {
        'startRowIndex': 1,
        'endRowIndex': 2,
        'startColumnIndex': 1,
        'endColumnIndex': 2
    }
    assert get_range_colorize(1, 2, 1, 2, 123456789) == expected
    assert get_range_colorize(sheet_id=123456789) == {"sheetId": 123456789}
    assert get_range_colorize(1, 2, 1, 2) == expected_2


def test_get_range_colorize_exceptions():

    with pytest.raises(TypeError):
        get_range_colorize([1], 2, 1, 2, 123456789)
    with pytest.raises(TypeError):
        get_range_colorize(1, {2}, 1, 2, 123456789)
    with pytest.raises(TypeError):
        get_range_colorize(1, 2, 1, 2, (123456789, ))
    with pytest.raises(TypeError):
        get_range_colorize('A', 'Text', 1, 2)

    with pytest.raises(ValueError):
        get_range_colorize(1, -1, 2, -2)
