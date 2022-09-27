import pytest

from data.google.get_body_methods.get_body import get_body_clear_conditions


def test_get_body_clear_conditions():
    expected_result = {
        "requests": [{
            "deleteConditionalFormatRule": {
                "index": 0,
                "sheetId": 12345678
            }}]}

    assert get_body_clear_conditions(12345678) == expected_result


def test_get_body_clear_conditions_exceptions():
    with pytest.raises(TypeError):
        get_body_clear_conditions('12345678')
        get_body_clear_conditions([])

    with pytest.raises(ValueError):
        get_body_clear_conditions('')
        