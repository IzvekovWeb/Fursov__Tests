from data.utils.functions import update_at
from domain.utils.valid_list import is_valid_list
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_top import OrdersTopReport

TOP_TABLE_START_COLUMN = 'C'
TOP_TABLE_END_COLUMN = 'Z'


class OrdersTopUseCase:
    """
    Отчет "Заказы (топ-500)"
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.update_at = None

    def execute(self, days_count: int = 8):
        suppliers = self.kwargs.get("suppliers")
        # Create an object of GoogleSheetAPI to work with Google Sheets
        spreadsheet_id = self.kwargs.get("Wildberries")
        sheet_title = "Топ-500"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        categories_list = []

        nomenclature_list = self.google_sheets_operate(table, categories_list)
        if not nomenclature_list:
            return

        orders_top = OrdersTopReport(days_count, nomenclature_list, suppliers=suppliers)
        orders_top.modify_dict(categories_list)

        # Get new data
        response = orders_top.execute()

        # Clear old datas
        table.clear(TOP_TABLE_START_COLUMN, TOP_TABLE_END_COLUMN)
        table.insert(response, TOP_TABLE_START_COLUMN, TOP_TABLE_END_COLUMN)

        self.update_at = update_at(response, table.insert)

        return self.update_at

    def google_sheets_operate(self, table, categories_list):
        result = table.get_column('A', 'B', 'Топ-500')

        result[0].pop(0)
        result[1].pop(0)

        categories_list.extend(result[1])

        categories_list.append('Остальное')
        categories_list.append('Итого')

        is_valid_list(result[0])

        return result[0]
