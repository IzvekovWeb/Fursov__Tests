from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_stocks_by_regions import StocksByRegionReport
from data.utils.functions import update_at


class StocksByRegionReportUseCase:
    """
    Остатки Регионы
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.update_at = None

    def execute(self) -> list:
        suppliers = self.kwargs.get("suppliers")
        spreadsheet_id = self.kwargs.get("Wildberries")
        sheet_title = "Остатки Регионы"
        sheet_id = self.kwargs.get(sheet_title)

        response = StocksByRegionReport(suppliers=suppliers).execute()

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()
        table.insert(response)

        self.update_at = update_at(response, table.insert)

        return self.update_at
