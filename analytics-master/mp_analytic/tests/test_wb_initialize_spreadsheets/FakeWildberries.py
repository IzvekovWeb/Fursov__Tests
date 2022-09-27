import os
from pathlib import Path

from data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets import read_from_json
from tests.test_GoogleSheetAPI.FakeService import GSA2
from config.constants import BASE_DIR


class FakeWildberries:
    def __init__(self, sheets, spreadsheet_title, spreadsheet_id):
        """
        The constructor of WildberriesSpreadSheet\n
        Create SpreadSheets with necessary sheets\n
        :param sheets: Dictionary of sheets' properties
        :param spreadsheet_title: SpreadSheet's title
        :param spreadsheet_id: SpreadSheet's ID
        """

        self.spreadsheet_id = spreadsheet_id
        self.__gsa = GSA2(sheet_title='sheet_title',
                          spreadsheet_title=spreadsheet_title,
                          spreadsheet_id=spreadsheet_id, )
        self.__sheets = sheets
        self.__manual_columns = read_from_json(os.path.join(Path.cwd().parent, "config", "manual_columns.json"))

    def run(self) -> str:
        """
        Run creating process\n
        :return: SpreadSheet's ID
        """
        return self.spreadsheet_id
