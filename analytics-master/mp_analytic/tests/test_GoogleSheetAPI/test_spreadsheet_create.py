from FakeService import GSA, FakeService, FakeGoogle, GetBySheetNameException
from expected import expected_spreadsheet_create


def fake_get_body_create_spreadsheet(title, sheet_title):
    body = {'properties': {'title': (title,), 'locale': 'ru_RU'}, 'sheets': [{'properties': {'sheetType': 'GRID', 'title': sheet_title,'gridProperties': {'rowCount': 1000,'columnCount': 26}}}]}
    return FakeGoogle().create(body).body


def test_spreadsheet_create(monkeypatch, GSA):
    GSA.spreadsheet_title = 'New'
    FGSA = FakeService()

    monkeypatch.setattr('data.google.sheet.sheet_api.get_body_create_spreadsheet', fake_get_body_create_spreadsheet)
    monkeypatch.setattr(GSA, 'service', FGSA.service)

    assert GSA.spreadsheet_create() == expected_spreadsheet_create


def test_spreadsheet_create_exception(monkeypatch, GSA):
    GSA.spreadsheet_title = 'New2'

    monkeypatch.setattr('data.google.sheet.sheet_api.get_body_create_spreadsheet', fake_get_body_create_spreadsheet)
    monkeypatch.setattr(GSA, 'service', GetBySheetNameException)

    assert GSA.spreadsheet_create() is False
