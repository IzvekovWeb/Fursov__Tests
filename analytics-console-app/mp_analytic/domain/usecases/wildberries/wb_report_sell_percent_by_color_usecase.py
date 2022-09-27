from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_report_sell_percent_by_color import SellPercentByColorReport


class SellPercentReportByColorUseCase:
    """
    Отчет "Процент выкупа (цвет)"
    """

    def execute(self) -> str:
        response = SellPercentByColorReport().execute()

        sheet_title = SHEETS.get('percent_color').get('title')
        sheet_id = SHEETS.get('percent_color').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)

        table.clear()
        table.insert(response)

        return table.get_sheet_url()
