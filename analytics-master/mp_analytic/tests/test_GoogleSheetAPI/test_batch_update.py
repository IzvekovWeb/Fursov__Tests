from FakeService import GSA, FakeService, GetBySheetNameException


def test_batch_update(monkeypatch, GSA):
    body = {'requests': [[{'repeatCell': {'range': 'Title!A1:A3', 'cell': {'userEnteredFormat': {'backgroundColor': {'red': 110, 'green': 200, 'blue': 1}}},'fields': 'userEnteredFormat.backgroundColor'}}]]}
    GSA.sheet_id = 94459280
    FDSA = FakeService()

    monkeypatch.setattr(GSA, 'service', FDSA.service)

    a = GSA.batch_update(body)
    assert isinstance(a, object)


def test_batch_update_exception(monkeypatch, GSA):
    body = {'requests': [[{'repeatCell': {'range': 'Title!A1:A3', 'cell': {'userEnteredFormat': {'backgroundColor': {'red': 110, 'green': 200, 'blue': 1}}},'fields': 'userEnteredFormat.backgroundColor'}}]]}

    GSA.sheet_id = 94459280
    monkeypatch.setattr(GSA, 'service', GetBySheetNameException)

    assert GSA.batch_update(body) is False
