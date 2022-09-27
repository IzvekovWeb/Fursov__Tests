from FakeService import GSA, FakeService, GetBySheetNameException
from expected import expected_get_column


def fake_get_range_column_row(a, b, c):
    return "sheet_title!A1:C5"


def test_get_column(monkeypatch, GSA):
    GSA.sheet_title = 'sheet_title'
    monkeypatch.setattr('data.google.sheet.sheet_api.get_range_column_row', fake_get_range_column_row)
    monkeypatch.setattr(GSA, 'service', FakeService().service)

    assert GSA.get_column('A1', 'C5', 'sheet_title') == expected_get_column


def test_get_column_not_values(monkeypatch, GSA):

    monkeypatch.setattr('data.google.sheet.sheet_api.get_range', fake_get_range_column_row)
    monkeypatch.setattr(GSA, 'service', FakeService().service)

    monkeypatch.setattr(GSA, 'call_function', lambda x: {'values': []})

    assert GSA.get_column('A1', 'C2', 'sheet_title') == []


def test_get_column_exceptions(monkeypatch, GSA):

    monkeypatch.setattr('data.google.sheet.sheet_api.get_range', fake_get_range_column_row)
    monkeypatch.setattr(GSA, 'service', GetBySheetNameException)

    assert GSA.get_column('A1', 'C2', 'sheet_title') == []
