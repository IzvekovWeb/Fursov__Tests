from data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets import is_multiple_header


def test_is_multiple_header():
    assert is_multiple_header('string') == ['string']

    assert is_multiple_header({'dict_key_1': 'val_1', 'dict_key_2': 2}) == ['val_1', 2]

    assert is_multiple_header(['list']) == ['list']

    assert is_multiple_header(123) == ['123']
