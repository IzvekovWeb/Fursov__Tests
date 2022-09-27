from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_report_sell_percent_by_subject import SellPercentBySubjectReport


class SellPercentReportBySubjectUseCase:
    """
    Отчет "Процент выкупа (предмет)"
    """

    def execute(self) -> str:
        response = SellPercentBySubjectReport().execute()

        sheet_title = SHEETS.get('percent_subject').get('title')
        sheet_id = SHEETS.get('percent_subject').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)

        table.clear()
        table.insert(response)

        return table.get_sheet_url()
