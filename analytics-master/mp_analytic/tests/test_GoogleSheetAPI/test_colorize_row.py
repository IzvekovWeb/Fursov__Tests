from FakeService import GSA


def fake_body(body=None, _range=None, _color=None):
    body["requests"].append([{"repeatCell": {"range": {'sheetId': 94459280}, "cell": { "userEnteredFormat": {"backgroundColor": {'red': 1.0, 'green': 1.0, 'blue': 1.0}}, }, "fields": "userEnteredFormat.backgroundColor" }}])


expected_no_body = {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'replies': [{}]}


def test_colorize_row_no_body(monkeypatch, GSA):
    GSA.sheet_title = 'Title'
    GSA.sheet_id = 94459280
    #
    monkeypatch.setattr('data.google.sheet.sheet_api.get_body_colorize', fake_body)
    monkeypatch.setattr('data.google.sheet.sheet_api.get_range_colorize', lambda sheet_id: 94459280)
    monkeypatch.setattr('data.google.sheet.sheet_api.WHITE', lambda z: {'red': 1.0, 'green': 1.0, 'blue': 1.0})

    assert GSA.colorize_row() == expected_no_body


def test_colorize_row(monkeypatch, GSA):
    GSA.sheet_title = 'Title'
    GSA.sheet_id = 94459280
    body = {"requests": []}
    fake_body(body)

    assert GSA.colorize_row(body) == expected_no_body


