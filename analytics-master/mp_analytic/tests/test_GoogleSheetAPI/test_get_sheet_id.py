from FakeService import GSA, FakeService


def test_get_sheet_id(monkeypatch, GSA):
    GSA.sheet_title = 'sheet_title'

    FGSA = FakeService()
    monkeypatch.setattr(GSA, 'service', FGSA.service)

    assert GSA.get_sheet_id('sheet_title') == 688346002
    assert GSA.get_sheet_id() == 688346002
