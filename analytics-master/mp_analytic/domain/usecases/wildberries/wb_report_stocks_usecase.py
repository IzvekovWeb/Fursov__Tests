from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_report_stocks import StocksReport
from data.utils.functions import update_at


class StocksUseCase:
    """
    Отчет "Отчет по остаткам на складах ВБ"
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs
        self.update_at = None

    def execute(self) -> str:
        suppliers = self.kwargs.get("suppliers")
        response = StocksReport(suppliers=suppliers).execute()

        spreadsheet_id = self.kwargs.get("Wildberries")
        sheet_title = "Остатки"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()
        table.insert(response)

        self.update_at = update_at(response, table.insert)

        return self.update_at
