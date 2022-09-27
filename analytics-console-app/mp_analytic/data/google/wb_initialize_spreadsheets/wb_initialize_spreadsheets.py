from config.constants import GOOGLE_SPREADSHEETS, GOOGLE_SPREADSHEETS_MIN, GOOGLE_SPREADSHEETS_OPT, GOOGLE_SHEETS_MANUAL
from data.google.manual_columns.wb_manual_insert_column import insert_header
from data.google.sheet.sheet_api import GoogleSheetAPI
from json import load


class WildberriesSpreadSheet(object):
    def __init__(self, sheets, spreadsheet_title, spreadsheet_id):
        """
        The constructor of WildberriesSpreadSheet\n
        Create SpreadSheets with necessary sheets\n
        :param sheets: Dictionary of sheets' properties
        :param spreadsheet_title: SpreadSheet's title
        :param spreadsheet_id: SpreadSheet's ID
        """

        self.__gsa = GoogleSheetAPI(sheet_title='sheet_title',
                                    spreadsheet_title=spreadsheet_title,
                                    spreadsheet_id=spreadsheet_id, )
        self.__sheets = sheets
        self.__manual_columns = read_from_json(GOOGLE_SHEETS_MANUAL)

    def run(self) -> str:
        """
        Run creating process\n
        :return: SpreadSheet's ID
        """

        self.__create_sheet()
        return self.__gsa.spreadsheet_id

    def __create_sheet(self):
        for sheet_name, properties in self.__sheets.items():
            self.__change_sheet_name(properties)
            sheet_id = self.__gsa.create_sheet()
            self.__change_properties(sheet_name, sheet_id)
            self.__is_manual(self.__gsa.sheet_title)

    def __change_properties(self, sheet_name, sheet_id):
        self.__sheets[sheet_name]['id'] = sheet_id

    def __change_sheet_name(self, properties):
        self.__gsa.sheet_title = properties['title']

    def __generate_columns_header(self, sheet_name):
        if sheet_name in self.__manual_columns.keys():
            return self.__manual_columns.get(sheet_name)
        return

    def __is_manual(self, sheet_name):
        headers = self.__generate_columns_header(sheet_name)
        if headers:
            insert_header(self.__gsa, is_multiple_header(headers))


def is_multiple_header(headers):
    if isinstance(headers, str):
        return [headers]
    elif isinstance(headers, dict):
        return list(headers.values())


def read_from_json(file) -> dict:
    with open(file, 'r') as json_file:
        return load(json_file)


def initialize_spreadsheets(tariff: int) -> dict:
    spreadsheet_choice = {
        1: GOOGLE_SPREADSHEETS_MIN,
        2: GOOGLE_SPREADSHEETS_OPT,
        3: GOOGLE_SPREADSHEETS
    }
    if tariff in (4, 5):
        tariff = 3
    spreadsheets = read_from_json(spreadsheet_choice.get(tariff))
    response = {}
    for key, spreadsheet in spreadsheets.items():
        spreadsheet['id'] = 0
        instance = WildberriesSpreadSheet(spreadsheet['sheets'],
                                          spreadsheet['title'],
                                          spreadsheet['id'])
        spreadsheet['id'] = instance.run()
        response[spreadsheet["title"]] = spreadsheet
    return response
