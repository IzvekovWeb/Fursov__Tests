from config.sheets import SHEETS, SPREADSHEET_ID
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dynamic_orders import DynamicOrdersReport
from data.utils.functions import update_at


class DynamicOrdersUseCase:
    """
    Динамика заказов поартикульно
    """

    def __init__(self):
        self.title = "Динамика заказов поартикульно"
        self.update_at = None
        self.dashboard_data = None

    def execute(self) -> str:
        sheet_title_count = SHEETS.get('dynamic_count').get('title')
        sheet_id_count = SHEETS.get('dynamic_count').get('id')

        sheet_title_rub = SHEETS.get('dynamic_rub').get('title')
        sheet_id_rub = SHEETS.get('dynamic_rub').get('id')

        report = DynamicOrdersReport()
        response = report.execute()

        table = GoogleSheetAPI(sheet_title_count, SPREADSHEET_ID, sheet_id_count)

        table.clear()
        table.clear(sheet_name=sheet_title_rub)

        table.insert(response[1])
        table.insert(response[0], sheet_name=sheet_title_rub)

        self.design(table, len(response))
        self.design(table, len(response), sheet_id_rub)

        self.update_at = update_at(response[1], table.insert)
        self.update_at = update_at(response[1], table.insert, sheet_name=sheet_title_rub)

        self.dashboard_data = report.get_drf_orders()

        return self.update_at

    def design(self, table, length, sheet_id=None):
        table.number_format(1, length, 5, 13, sheet_id=sheet_id)
