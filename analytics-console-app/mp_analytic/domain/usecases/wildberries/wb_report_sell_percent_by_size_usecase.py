from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_report_sell_percent_by_size import SellPercentReportBySize


class SellPercentReportBySizeUseCase:
    """
    Отчет "Процент выкупа (предмет)"
    """

    def execute(self) -> str:
        response = SellPercentReportBySize().execute()

        sheet_title = SHEETS.get('percent_size').get('title')
        sheet_id = SHEETS.get('percent_size').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)

        table.clear()
        table.insert(response)

        return table.get_sheet_url()
