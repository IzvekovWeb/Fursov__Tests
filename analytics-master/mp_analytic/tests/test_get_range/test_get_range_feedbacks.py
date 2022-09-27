import pytest

from data.google.get_range_methods.get_range import get_range_feedbacks


def test_get_range_feedbacks():
    expected = {
        "sheetId": 12345678,
        "startRowIndex": 1,
        "endRowIndex": 2,
        "startColumnIndex": 6,
        "endColumnIndex": 10,
    }
    assert get_range_feedbacks(12345678, 1) == expected

    expected_2 = {
        "sheetId": 555111,
        "startRowIndex": 10,
        "endRowIndex": 11,
        "startColumnIndex": 6,
        "endColumnIndex": 10,
    }
    assert get_range_feedbacks(555111, 10) == expected_2

    assert get_range_feedbacks(555111) == {"sheetId": 555111}


def test_get_range_feedbacks_exceptions():

    with pytest.raises(TypeError):
        get_range_feedbacks(555111, 'int only')
        get_range_feedbacks([1234567])

    with pytest.raises(ValueError):
        get_range_feedbacks(12345678, -10)
