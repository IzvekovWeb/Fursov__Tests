from data.utils.functions import update_at
from domain.utils.valid_list import is_valid_list
from config.sheets import SHEETS, SPREADSHEET_ID
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_top import OrdersTopReport

TOP_TABLE_START_COLUMN = 'C'
TOP_TABLE_END_COLUMN = 'Z'


class OrdersTopUseCase:
    """
    Отчет "Заказы (топ-500)"
    """

    def __init__(self):
        self.title = "Топ-500"
        self.url = None
        self.update_at = None

    def execute(self, days_count: int = 8) -> str:
        # Create an object of GoogleSheetAPI to work with Google Sheets
        sheet_title = SHEETS.get('top500').get('title')
        sheet_id = SHEETS.get('top500').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID, sheet_id)

        categories_list = []

        nomenclature_list = self.google_sheets_operate(table, categories_list)
        orders_top = OrdersTopReport(days_count, nomenclature_list)
        orders_top.modify_dict(categories_list)

        # Get new data
        response = orders_top.execute()

        # Clear old datas
        table.clear(TOP_TABLE_START_COLUMN, TOP_TABLE_END_COLUMN)
        table.insert(response, TOP_TABLE_START_COLUMN, TOP_TABLE_END_COLUMN)

        self.update_at = update_at(response, table.insert)

        self.url = table.get_sheet_url()
        return self.url

    def google_sheets_operate(self, table, categories_list):
        # Get Categories and Nomenclatures
        result = table.get_column('A', 'B', 'Топ-500')

        result[0].pop(0)
        result[1].pop(0)

        categories_list.extend(result[0])

        categories_list.append('Остальное')
        categories_list.append('Итого')

        is_valid_list(result[1])

        return result[1]


if __name__ == '__main__':
    OrdersTopUseCase().execute()