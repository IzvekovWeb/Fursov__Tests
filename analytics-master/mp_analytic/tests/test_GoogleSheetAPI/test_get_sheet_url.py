from FakeService import GSA


def test_get_sheet_url(GSA):

    expected_1 = 'https://docs.google.com/spreadsheets/d/12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo/edit#gid=94459280'
    assert GSA.get_sheet_url() == expected_1

    GSA.spreadsheet_id = '1gvFpgZnWE79mX5C2GtQ1hEUIukmJjRY9T7jko9W9EOE'
    GSA.sheet_id = 325467938

    expected_2 = 'https://docs.google.com/spreadsheets/d/1gvFpgZnWE79mX5C2GtQ1hEUIukmJjRY9T7jko9W9EOE/edit#gid=325467938'
    assert GSA.get_sheet_url() == expected_2
