import pytest

from FakeService import GSA
from expected import expected_empty_reply


def fake_update_borders(*args, **kwargs):
    return {'requests': [{'updateBorders': {'range': {'sheetId': '94459280', 'startRowIndex': 1, 'endRowIndex': 2, 'startColumnIndex': 1, 'endColumnIndex': 4}, 'left': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.0, 'green': 0.0, 'blue': 0.0}}, 'right': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.0, 'green': 0.0, 'blue': 0.0}}, 'bottom': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.0, 'green': 0.0, 'blue': 0.0}}, 'top': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.0, 'green': 0.0, 'blue': 0.0}}}}]}


def test_borders(monkeypatch, GSA):
    monkeypatch.setattr('data.google.sheet.sheet_api.update_borders', fake_update_borders)

    assert GSA.borders() == expected_empty_reply

    assert GSA.borders(1, 2, 1, 4) == expected_empty_reply


# def test_borders_exceptions(monkeypatch, GSA):
#     with pytest.raises(TypeError):
#         GSA.borders(1, 2, 1, 4)
