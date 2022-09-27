from config.sheets import SHEETS, SPREADSHEET_ID
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_report_stocks import StocksReport
from data.utils.functions import update_at


class StocksUseCase:
    """
    Отчет "Отчет по остаткам на складах ВБ"
    """
    def __init__(self):
        self.title = "Отчет по остаткам на складах ВБ"
        self.update_at = None

    def execute(self) -> str:
        response = StocksReport().execute()
        sheet_title = SHEETS.get('remains').get('title')
        sheet_id = SHEETS.get('remains').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID, sheet_id)

        table.clear()
        table.insert(response)

        self.update_at = update_at(response, table.insert)

        return self.update_at
