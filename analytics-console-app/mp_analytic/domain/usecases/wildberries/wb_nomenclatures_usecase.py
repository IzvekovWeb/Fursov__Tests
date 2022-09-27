import datetime

from config.constants import WB_TOKEN
from config.sheets import SHEETS, SPREADSHEET_NM
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_nomenclatures import NomenclaturesReport


class NomenclaturesUseCase:
    """
    Отчет заказы по товарам (шт)
    """

    def execute(self) -> str:
        response = NomenclaturesReport(WB_TOKEN).execute()

        sheet_title = SHEETS.get('nomenclatures').get('title')
        sheet_id = SHEETS.get('nomenclatures').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_NM, sheet_id)
        table.clear()
        table.insert(response)
        table.insert([[f'ДАТА ОБНОВЛЕНИЯ: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}']], start_column='H')
        return table.get_sheet_url()


if __name__ == '__main__':
    NomenclaturesUseCase().execute()
