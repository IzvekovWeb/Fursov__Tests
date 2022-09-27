from FakeService import GSA, FakeService, GetBySheetNameException
from expected import expected_clear


def fake_get_range(a, b, c):
    return "'sheet_title'!A1:C2"


def fake_get_range_no_title(a, b, c):
    return "'Empty title'!A1:C2"


def test_clear(monkeypatch, GSA):
    GSA.sheet_title = 'sheet_title'
    monkeypatch.setattr('data.google.sheet.sheet_api.get_range', fake_get_range)
    monkeypatch.setattr(GSA, 'service', FakeService().service)

    assert GSA.clear('A1', 'C2', 'sheet_title') == expected_clear


def test_clear_no_title(monkeypatch, GSA):

    monkeypatch.setattr('data.google.sheet.sheet_api.get_range', fake_get_range_no_title)
    monkeypatch.setattr(GSA, 'service', FakeService().service)

    GSA.sheet_title = 'Empty title'

    assert GSA.clear('A1', 'C2') == expected_clear


def test_clear_exceptions(monkeypatch, GSA):

    monkeypatch.setattr('data.google.sheet.sheet_api.get_range', fake_get_range)
    monkeypatch.setattr(GSA, 'service', GetBySheetNameException)

    assert GSA.clear('A1', 'C2', 'sheet_title') is False
