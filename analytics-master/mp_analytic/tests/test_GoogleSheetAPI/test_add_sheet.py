from FakeService import FakeService, GSA
from tests.test_GoogleSheetAPI.expected import *


def fake_get_body_add_sheet(sheet_title):
    return {'requests': [{'addSheet': {'properties': {'sheetType': 'GRID', 'title': 'sheet_title', 'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}}]}


def fake_batch_update(body):
    class Batch(object):
        def execute(self):
            return {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'replies': [{'addSheet': {'properties': {'sheetId': 854162543, 'title': 'sheet_title', 'index': 3, 'sheetType': 'GRID', 'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}}]}
    return Batch().execute


def test_add_sheet(monkeypatch, GSA):
    FGSA = FakeService()

    monkeypatch.setattr('data.google.sheet.sheet_api.get_body_add_sheet', fake_get_body_add_sheet)
    monkeypatch.setattr(GSA, 'service', FGSA.service)
    monkeypatch.setattr(GSA, 'batch_update', fake_batch_update)

    assert GSA.add_sheet() == expected_add_sheet


def test_add_sheet_exceptions(monkeypatch, GSA):

    monkeypatch.setattr(GSA, 'batch_update', lambda x: lambda: False)

    assert GSA.add_sheet() is False
