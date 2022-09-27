from FakeService import GSA, fake_batch_update
from expected import expected_empty_reply


def test_colorize_dynamic(monkeypatch, GSA):
    body = {'requests': [[{'repeatCell': {'range': 'Title!A1:A3', 'cell': {'userEnteredFormat': {'backgroundColor': {'red': 110, 'green': 200, 'blue': 1}}}, 'fields': 'userEnteredFormat.backgroundColor'}}]]}

    GSA.sheet_id = 94459280
    monkeypatch.setattr(GSA, 'batch_update', fake_batch_update)

    assert GSA.colorize_dynamic(body) == expected_empty_reply
