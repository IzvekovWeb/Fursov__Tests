from FakeService import GSA, FakeService


def fake_get_range(a, b, c):
    return "sheet_title!A1:C5"


def fake_get_body_insert(a, b):
    return {"valueInputOption": "USER_ENTERED", "data": [{"range": "'sheet_title'!A1:C5", "values": [[1], [22], [33]]}]}


def test_insert(monkeypatch, GSA):
    monkeypatch.setattr('data.google.sheet.sheet_api.get_body_insert', fake_get_body_insert)
    monkeypatch.setattr(GSA, 'service', FakeService().service)

    assert GSA.insert([[1], [22], [33]], 'A1', 'C5', 'sheet_title') is True


def test_insert_not_values(monkeypatch, GSA):

    monkeypatch.setattr('data.google.sheet.sheet_api.get_body_insert', fake_get_body_insert)
    monkeypatch.setattr(GSA, 'service', FakeService().service)

    monkeypatch.setattr(GSA, 'call_function', lambda x: {'totalUpdatedCells': 0})

    assert GSA.insert('A1', 'C2', 'sheet_title') is False
