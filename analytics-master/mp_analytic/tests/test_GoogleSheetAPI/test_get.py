from FakeService import GSA, FakeService, GetBySheetNameException

expected_get = [['11', '12'], ['21', '22']]


def test_get(monkeypatch, GSA):
    FGSA = FakeService()

    monkeypatch.setattr(GSA, 'service', FGSA.service)

    assert GSA.get('Title') == expected_get


def test_get_no_title(monkeypatch, GSA):
    FGSA = FakeService()

    monkeypatch.setattr(GSA, 'service', FGSA.service)

    assert GSA.get('This title is not created') == []


def test_get_exceptions(monkeypatch, GSA):

    monkeypatch.setattr(GSA, 'service', GetBySheetNameException)

    assert GSA.get('Title') == []
