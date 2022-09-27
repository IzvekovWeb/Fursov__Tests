from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dispatch import Dispatch
from data.utils.functions import update_at


class DispatchUseCase:
    """
    Отгрузка
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.update_at = None

    def execute(self, days_count=7) -> str:
        suppliers = self.kwargs.get("suppliers")
        response = Dispatch(days_count, suppliers=suppliers).execute()

        spreadsheet_id = self.kwargs.get("Wildberries 2")
        sheet_title = "Отгрузка"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()
        table.insert(response)

        self.update_at = update_at(response, table.insert)

        return self.update_at
