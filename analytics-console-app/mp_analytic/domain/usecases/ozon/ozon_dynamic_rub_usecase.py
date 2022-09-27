from config.sheets import SHEETS_OZON, SPREADSHEET_OZON
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.ozon.ozon_dynamic_rub import OzonDynamicRub


class OzonDynamicRubUseCase:
    def __init__(self):
        self.__sheet_title = SHEETS_OZON.get('dynamic_rub').get('title')
        self.__sheet_id = SHEETS_OZON.get('dynamic_rub').get('id')

        self.__table = GoogleSheetAPI(self.__sheet_title, SPREADSHEET_OZON, self.__sheet_id)

    def execute(self) -> str:
        response = OzonDynamicRub().execute()

        self.__table.clear()
        self.__table.insert(response)
        return self.__table.get_sheet_url()
