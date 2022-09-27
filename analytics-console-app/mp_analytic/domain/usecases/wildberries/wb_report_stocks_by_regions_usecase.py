from config.sheets import SHEETS, SPREADSHEET_ID
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_stocks_by_regions import StocksByRegionReport
from data.utils.functions import update_at


class StocksByRegionReportUseCase:
    """
    Отчет "Остатки Регионы"
    """
    def __init__(self):
        self.title = "Остатки Регионы"
        self.url = None
        self.update_at = None

    def execute(self) -> list:
        sheet_title = SHEETS.get('region_remains').get('title')
        sheet_id = SHEETS.get('region_remains').get('id')

        response = StocksByRegionReport().execute()

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID, sheet_id)

        table.clear()
        table.insert(response)

        self.update_at = update_at(response, table.insert)

        self.url = table.get_sheet_url()

        return [self.title, self.url]
