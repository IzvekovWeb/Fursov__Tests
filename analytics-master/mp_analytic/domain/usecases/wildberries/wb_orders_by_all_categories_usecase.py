from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dynamic_category import DynamicCategoryReport
from data.utils.functions import update_at


class OrdersByAllCategoriesUseCase:
    """
    Динамика заказов по всем категориям, руб
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.update_at = None
        self.dashboard_data = None

    def execute(self) -> str:
        suppliers = self.kwargs.get("suppliers")
        report = DynamicCategoryReport(suppliers=suppliers)
        response = report.execute()

        spreadsheet_id = self.kwargs.get("Wildberries")
        sheet_title = "Заказы (все категории)"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)
        table.clear()
        table.insert(response)

        self.update_at = update_at(response, table.insert)

        self.dashboard_data = report.get_drf_orders()

        return self.update_at
