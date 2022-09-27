import pytest
import os

from pathlib import Path
from config.constants import BASE_DIR
from data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets import is_multiple_header, read_from_json

expected_json_1 = {"some_key": "str","dict_key": { "int_value": 123}}
file_path_1 = os.path.join(Path.cwd().parent, "tests", "test_wb_initialize_spreadsheets", "jsons", "test_json_file.json")

expected_json_2 = {"some_key": "русский","dict_key": { "int_value": 123}}
file_path_2 = os.path.join(Path.cwd().parent, "tests", "test_wb_initialize_spreadsheets", "jsons", "test_json_file_ru.json")


def test_read_from_json():

    assert read_from_json(file_path_1) == expected_json_1

    assert read_from_json(file_path_2) == expected_json_2

    assert isinstance(read_from_json(file_path_2), dict)


def test_read_from_json_path():

    with pytest.raises(OSError):
        read_from_json('some_failed_path')
