import pytest

from data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets import WildberriesSpreadSheet
from tests.test_GoogleSheetAPI.FakeService import GSA2, GSA
from json import loads


@pytest.fixture
def sheets(GSA):
    file_path = "C:\\Users\\sasiz\\Desktop\\Работа\\Fursov\\analytics-master\\mp_analytic\\config\\spreadsheets_min.json"
    with open(file_path, 'r', encoding='utf8') as file:
        sheets = file.read()
    sheets = loads(sheets)
    sheets['SPREADSHEET_ID']['id'] = GSA.spreadsheet_id
    return sheets


def test_init(monkeypatch, GSA, sheets):
    GSA.sheet_id = 94459280
    GSA.sheet_title = 'sheet_title'

    monkeypatch.setattr('data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets.GoogleSheetAPI', GSA2)
    monkeypatch.setattr('data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets.GOOGLE_SHEETS_MANUAL',
                        'C:\\Users\\sasiz\\Desktop\\Работа\\Fursov\\analytics-master\\mp_analytic\\config\\manual_columns.json')

    WS = WildberriesSpreadSheet(sheets, GSA.spreadsheet_title, GSA.spreadsheet_id)

    assert isinstance(WS, WildberriesSpreadSheet) is True


def test_run(monkeypatch, GSA, sheets):
    GSA.sheet_id = 94459280
    GSA.sheet_title = 'sheet_title'

    monkeypatch.setattr('data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets.GoogleSheetAPI', GSA2)
    monkeypatch.setattr('data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets.GOOGLE_SHEETS_MANUAL',
                        'C:\\Users\\sasiz\\Desktop\\Работа\\Fursov\\analytics-master\\mp_analytic\\config\\manual_columns.json')

    WS = WildberriesSpreadSheet(sheets, GSA.spreadsheet_title, GSA.spreadsheet_id)

    assert WS.run() == GSA.spreadsheet_id
