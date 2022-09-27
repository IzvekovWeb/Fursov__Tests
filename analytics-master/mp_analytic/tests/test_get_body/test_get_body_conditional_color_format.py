import pytest

from data.google.get_body_methods.get_body import get_body_conditional_color_format


def test_get_body_conditional_color_format():
    expected_result_1 = {'requests': [{
        "addConditionalFormatRule": {
            "rule": {
                "ranges": [{
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 1
                }],
                "gradientRule": {
                    "minpoint": {
                        "color": {'green': 1},
                        "type": "MIN"
                    },
                    "midpoint": {
                        "color": {'red': 100},
                        "type": "PERCENTILE",
                        "value": "50",
                    },
                    "maxpoint": {
                        "color": {'green': 1, 'blue': 10},
                        "type": "MAX"
                    }}},
            "index": 0
        }}]}

    assert get_body_conditional_color_format(
        0,
        0,
        1,
        {'green': 1},
        {'red': 100},
        {'green': 1, 'blue': 10}
    ) == expected_result_1

    expected_result_2 = {'requests': [{
        "addConditionalFormatRule": {
            "rule": {
                "ranges": [{
                    "sheetId": '12345678',
                    "startRowIndex": 13,
                    "endRowIndex": 22
                }],
                "gradientRule": {
                    "minpoint": {
                        "color": {'red': 255, 'green': 1, 'blue': 100},
                        "type": "MIN"
                    },
                    "midpoint": {
                        "color": {'red': 255},
                        "type": "PERCENTILE",
                        "value": "50",
                    },
                    "maxpoint": {
                        "color": {'green': 0, 'blue': 220},
                        "type": "MAX"
                    }}},
            "index": 0
        }}]}

    assert get_body_conditional_color_format(
        '12345678',
        13,
        22,
        {'red': 255, 'green': 1, 'blue': 100},
        {'red': 255},
        {'green': 0, 'blue': 220}
    ) == expected_result_2


def test_get_body_conditional_color_format_exceptions():
    with pytest.raises(TypeError):
        get_body_conditional_color_format(
            0,
            0,
            1,
            255,
            {'red': 100},
            {'green': 1, 'blue': 10}
        )

        get_body_conditional_color_format(
            0,
            0,
            1,
            {'red': 100, 'green': 255, 'blue': 50},
            ['red_255'],
            {'green': 1, 'blue': 10}
        )

        get_body_conditional_color_format(
            0,
            0,
            1,
            {'red': 100},
            {'red': 100, 'blue': 123, 'green': 255},
            'green 100'
        )
        get_body_conditional_color_format(
            0,
            1,
            1,
            {'red': 255},
            {'red': 255, 'blue': 233, 'green': 255},
            {'red': 'text'},
        )

    with pytest.raises(ValueError):
        get_body_conditional_color_format(
            'some_kind',
            0,
            1,
            {},
            {'red': 100},
            {'green': 1, 'blue': 10}
        )

    with pytest.raises(ValueError):
        get_body_conditional_color_format(
            0,
            -1,
            -5,
            {'red': 100},
            {'red': 100, 'blue': 123, 'green': 255},
            {'red': 255}
        )

        get_body_conditional_color_format(
            0,
            1,
            1,
            {'red': 600},
            {'red': -1, 'blue': 233, 'green': 255},
            {'red': 255},
        )
