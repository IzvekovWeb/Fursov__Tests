import pytest

from data.google.utils.constructors import border_constructor

expected_result_1 = {"style": 'DOTTED', "width": 10, "color": {}}
expected_result_2 = {"style": 'DASHED', "width": 120, "color": {'red': 0, 'green': 0, 'blue': 0}}
expected_result_3 = {"style": 'NONE', "width": 0, "color": {}}


@pytest.mark.parametrize("style, width, color, expected", [
    ('DOTTED', 10, {}, expected_result_1),
    ('DASHED', 120, {'red': 0, 'green': 0, 'blue': 0}, expected_result_2),
    (None, 0, {}, expected_result_3)
])
def test_border_constructor(style, width, color, expected):
    assert border_constructor(style, width, color) == expected


def test_border_constructor_exceptions():

    with pytest.raises(TypeError):
        border_constructor([], 2, {})
        border_constructor('', [], {})
        border_constructor('', 2, [])
    with pytest.raises(ValueError):
        border_constructor('DASHED2', 2, {})
        border_constructor('DASHED', -1, {})
    with pytest.raises(TypeError):
        border_constructor('DASHED', '', '')
