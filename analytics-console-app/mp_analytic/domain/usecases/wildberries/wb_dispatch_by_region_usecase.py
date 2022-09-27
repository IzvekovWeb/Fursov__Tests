from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dispatch_by_region import DispatchBYRegion
from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.utils.functions import update_at


class DispatchByRegionUseCase:
    """
    Отгрузка
    """
    def __init__(self):
        self.update_at = None

    def execute(self) -> str:
        response = DispatchBYRegion().execute()

        sheet_title = SHEETS.get('dispatch_by_region').get('title')
        sheet_id = SHEETS.get('dispatch_by_region').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)

        table.clear()
        table.insert(response)

        self.update_at = update_at(response, table.insert)


if __name__ == '__main__':
    DispatchByRegionUseCase().execute()

