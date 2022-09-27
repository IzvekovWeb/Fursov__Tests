from FakeService import GSA
from expected import expected_spreadsheet_create

expected_create_sheet_new = {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'replies': [{'addSheet': {'properties': {'sheetId': 1171942659, 'title': 'New Title', 'index': 4, 'sheetType': 'GRID', 'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}}]}


def test_create_sheet(monkeypatch, GSA):
    GSA.sheet_title = 'New Title'

    monkeypatch.setattr(GSA, 'add_sheet', lambda: expected_create_sheet_new)
    monkeypatch.setattr(GSA, 'get_sheet_id', lambda x: 1171942659)

    assert GSA.create_sheet() == 1171942659


def test_create_sheet_no_spreadsheet(monkeypatch, GSA):
    GSA.spreadsheet_id = ''

    monkeypatch.setattr(GSA, 'spreadsheet_create', lambda: expected_spreadsheet_create)
    monkeypatch.setattr(GSA, 'access_for_new_table', lambda: print('Access granted'))
    monkeypatch.setattr(GSA, 'get_sheet_id', lambda x: 741948705)

    assert GSA.create_sheet() == 741948705



# Тест функции access_for_new_table неизбежно делает запрос в google
# так как это неверно с точки зрения тестирования
# тест не доделан
# def not_work_test_access_for_new_table(GSA):
#     GSA.spreadsheet_id = '1gvFpgZnWE79mX5C2GtQ1hEUIukmJjRY9T7jko9W9EOE'
#     GSA.access_for_new_table()
#
#     drive_service.permissions().list(fileId='1gvFpgZnWE79mX5C2GtQ1hEUIukmJjRY9T7jko9W9EOE').execute()
#     result = {'kind': 'drive#permissionList',
#                 'permissions': [{'allowFileDiscovery': False,
#                   'id': 'anyoneWithLink',
#                   'kind': 'drive#permission',
#                   'role': 'writer',
#                   'type': 'anyone'},
#                  {'id': '04934051511918253849',
#                   'kind': 'drive#permission',
#                   'role': 'owner',
#                   'type': 'user'}]}
