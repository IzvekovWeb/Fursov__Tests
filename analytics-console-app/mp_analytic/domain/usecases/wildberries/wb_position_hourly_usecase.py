from config.sheets import SHEETS, SPREADSHEET_ID
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_position_hourly import PositionHourly
from data.utils.functions import update_at
from domain.utils.valid_list import is_valid_list


class PositionHourlyUseCase:
    """
        Отчет "Позиции Ежечасно"
    """

    def __init__(self):
        self.title = "Позиции Ежечасно"
        self.url = None
        self.update_at = None

    def execute(self):
        title = SHEETS['position_hour']['title']
        sheet_id = SHEETS['position_hour']['id']

        table = GoogleSheetAPI(title, SPREADSHEET_ID, sheet_id)
        search_query, nomenclature_list = self.google_sheets_operate(table)

        response = PositionHourly(search_query=search_query, nomenclature_list=nomenclature_list).execute()

        table.clear(start_column='C')

        table.insert(response, start_column='C')

        self.update_at = update_at(response, table.insert)

        self.url = table.get_sheet_url()
        return self.url

    def google_sheets_operate(self, table):
        search_query = table.get_column('A')
        nomenclatures = table.get_column('B')

        search_query[0].pop(0)
        nomenclatures[0].pop(0)

        is_valid_list(nomenclatures[0])

        return search_query[0][0], nomenclatures[0]
