import datetime

from config.constants import WB_TOKEN
from config.sheets import SHEETS, SPREADSHEET_ID_SECOND, SPREADSHEET_ID_ACCOUNTING
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dispatch import Dispatch
from data.utils.functions import update_at


class DispatchUseCase:
    """
    Отчет заказы по товарам (шт)
    """
    def __init__(self):
        self.update_at = None

    def execute(self, days_count=7) -> str:
        sheet_title = SHEETS.get('accounting').get('title')
        sheet_id = SHEETS.get('accounting').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_ACCOUNTING, sheet_id)
        table = table.get()
        response = Dispatch(days_count, WB_TOKEN).execute(table[1:])

        sheet_title = SHEETS.get('dispatch').get('title')
        sheet_id = SHEETS.get('dispatch').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)
        table.clear()
        table.insert(response)
        self.update_at = update_at(response, table.insert)


if __name__ == '__main__':
    DispatchUseCase().execute()
