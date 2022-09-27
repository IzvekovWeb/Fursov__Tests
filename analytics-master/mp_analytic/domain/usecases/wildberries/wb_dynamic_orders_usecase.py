from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dynamic_orders import DynamicOrdersReport
from data.utils.functions import update_at


class DynamicOrdersUseCase:
    """
    Динамика заказов поартикульно
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.update_at = None
        self.dashboard_data = None

    def execute(self) -> str:
        suppliers = self.kwargs.get("suppliers")
        spreadsheet_id = self.kwargs.get("Wildberries")
        sheet_title_count = "Динамика (шт)"
        sheet_id_count = self.kwargs.get(sheet_title_count)

        sheet_title_rub = "Динамика (руб)"
        sheet_id_rub = self.kwargs.get(sheet_title_rub)

        report = DynamicOrdersReport(suppliers=suppliers)
        response = report.execute()

        table = GoogleSheetAPI(sheet_title_count, spreadsheet_id, sheet_id_count)

        table.clear()
        table.clear(sheet_name=sheet_title_rub)

        table.insert(response[1])
        table.insert(response[0], sheet_name=sheet_title_rub)

        self.design(table, len(response))
        self.design(table, len(response), sheet_id_rub)

        self.update_at = update_at(response[0], table.insert)
        self.update_at = update_at(response[1], table.insert, sheet_name=sheet_title_rub)

        self.dashboard_data = report.get_drf_orders()

        return self.update_at

    def design(self, table, length, sheet_id=None):
        table.number_format(1, length, 5, 13, sheet_id=sheet_id)
