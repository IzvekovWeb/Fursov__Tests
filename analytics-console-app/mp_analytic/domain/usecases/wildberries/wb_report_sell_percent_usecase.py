from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_report_sell_percent import SellPercentReport
from data.utils.functions import update_at


class SellPercentReportUseCase:
    """
    Отчет "Процент выкупа"
    """

    def __init__(self):
        self.title = "Процент выкупа"
        self.url = None
        self.update_at = None

    def execute(self) -> str:
        response = SellPercentReport().execute()

        sheet_id = SHEETS.get('percent_color').get('id')

        sheet_title_color = SHEETS.get('percent_color').get('title')
        sheet_title_subject = SHEETS.get('percent_subject').get('title')
        sheet_title_article = SHEETS.get('percent_article').get('title')
        sheet_title_size = SHEETS.get('percent_size').get('title')

        table = GoogleSheetAPI(sheet_title_color, SPREADSHEET_ID_SECOND, sheet_id)

        table.clear()
        table.clear(sheet_name=sheet_title_subject)
        table.clear(sheet_name=sheet_title_article)
        table.clear(sheet_name=sheet_title_size)

        table.insert(response[0])
        update_at(response[0], table.insert)

        table.insert(response[1], sheet_name=sheet_title_subject)
        update_at(response[1], table.insert, sheet_name=sheet_title_subject)

        table.insert(response[2], sheet_name=sheet_title_article)
        update_at(response[2], table.insert, sheet_name=sheet_title_article)

        table.insert(response[3], sheet_name=sheet_title_size)
        self.update_at = update_at(response[3], table.insert, sheet_name=sheet_title_size)

        self.url = table.get_sheet_url()
        return self.url
