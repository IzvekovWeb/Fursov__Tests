from FakeService import GSA, FakeService


def test_if_exists(monkeypatch, GSA):
    FGSA = FakeService()
    monkeypatch.setattr(GSA, 'service', FGSA.service)

    assert GSA.if_exists('sheet_title') is True
    assert GSA.if_exists('Title_not_exists') is False


def test_if_exists_exceptions(monkeypatch, GSA):

    FGSA = FakeService()
    monkeypatch.setattr(GSA, 'service', FGSA.service)
    monkeypatch.setattr(GSA.service, 'spreadsheets', FGSA.service.raiseException)

    assert GSA.if_exists('sheet_title') is False
