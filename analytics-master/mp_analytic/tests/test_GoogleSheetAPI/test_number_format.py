from FakeService import GSA, fake_batch_update
from expected import expected_empty_reply


def test_number_format(monkeypatch, GSA):
    GSA.sheet_title = 'Title'
    GSA.sheet_id = 94459280

    monkeypatch.setattr(GSA, 'batch_update', fake_batch_update)

    assert GSA.number_format(1, 2, 1, 4) == expected_empty_reply
