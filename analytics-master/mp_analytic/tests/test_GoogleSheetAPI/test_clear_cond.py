from FakeService import GSA, fake_batch_update
from expected import expected_empty_reply


def test_clear_cond(monkeypatch, GSA):
    GSA.sheet_id = 0
    GSA.spreadsheet_id = '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo'

    # monkeypatch.setattr(GSA, 'batch_update', fake_batch_update)
    #
    # assert GSA.clear_cond() == expected_empty_reply

    GSA.conditional_color_format(3, 4)

    GSA.get_spreasheet
