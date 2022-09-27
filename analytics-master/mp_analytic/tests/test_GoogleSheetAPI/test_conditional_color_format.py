from FakeService import GSA

expected = {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'replies': [{}]}


def test_conditional_color_format(monkeypatch, GSA):
    GSA.sheet_title = 'Title'
    GSA.sheet_id = 94459280

    assert GSA.conditional_color_format(1, 7) == expected
