import pytest

from data.google.get_body_methods.get_body import get_body_insert


def test_get_body_insert():

    expected_result_1 = {
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": "'Лист 1'!A1:B1", "values": [[123, '444']]}]}
    assert get_body_insert("'Лист 1'!A1:B1", [[123, '444']]) == expected_result_1

    expected_result_3 = {
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": "A1:B1", "values": [[123, '444']]}]}

    assert get_body_insert("A1:B1", [[123, '444']]) == expected_result_3

    expected_result_4 = {
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": "Лист1", "values": [[123, '444']]}]}
    assert get_body_insert("Лист1", [[123, '444']]) == expected_result_4


def test_get_body_insert_exceptions():

    with pytest.raises(TypeError):
        get_body_insert("'Лист1'!A1:B1", [123, '444'])
        get_body_insert("'Лист1'!A1:B1", {"A1": 123})
        get_body_insert("'Лист1'!A1:B1", (123, 234))
        get_body_insert("'Лист1'!A1:B1", '123 456')

    with pytest.raises(TypeError):
        get_body_insert(["'Лист1'!A1:B1"], [[123, '444']])
