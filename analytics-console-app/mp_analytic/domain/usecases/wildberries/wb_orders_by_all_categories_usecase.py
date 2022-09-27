from config.constants import WB_TOKEN
from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dynamic_category import DynamicCategoryReport


class OrdersByAllCategoriesUseCase:
    """
    Отчет "Заказы (все категории)"
    """
    def __init__(self):
        self.title = "Динамика заказов по всем категориям, руб"
        self.update_at = None
        self.dashboard_data = None

    def execute(self) -> str:
        report = DynamicCategoryReport(WB_TOKEN)
        response = report.execute()

        sheet_title = SHEETS.get('orders_all_categories').get('title')
        sheet_id = SHEETS.get('orders_all_categories').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)
        table.clear()
        table.insert(response)

        self.dashboard_data = report.get_drf_orders()

        return table.get_sheet_url()


if __name__ == '__main__':
    OrdersByAllCategoriesUseCase().execute()
