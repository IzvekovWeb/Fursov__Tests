from data.utils.functions import update_at
from config.sheets import SHEETS, SPREADSHEET_ID
from data.google.get_body_methods.get_body import get_body_feedbacks
from data.google.get_range_methods.get_range import get_range_feedbacks
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_report_feedback import FeedbackReport


class FeedbackReportUseCase:
    """
    Отчет "Отзывы"
    """
    def __init__(self):
        self.title = "Отзывы"
        self.url = None
        self.update_at = None

    def execute(self) -> str:
        response = FeedbackReport().execute()

        sheet_title = SHEETS.get('feedbacks').get('title')
        sheet_id = SHEETS.get('feedbacks').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID, sheet_id)

        table.clear()
        table.insert(response)

        self.clear_red_text(table)
        self.google_sheets_operate(table, response)

        self.update_at = update_at(response, table.insert)

        self.url = table.get_sheet_url()
        return self.url

    def google_sheets_operate(self, table, response):
        body = {"requests": []}

        for row, value in enumerate(response):
            if isinstance(value[6], int):
                if value[6] < 5:
                    _range = get_range_feedbacks(table.sheet_id, row)
                    get_body_feedbacks(body, _range)

        table.colorize_dynamic(body)

    def clear_red_text(self, table):
        body = {"requests": []}
        _range = get_range_feedbacks(table.sheet_id)
        get_body_feedbacks(body, _range, red=0)
        table.colorize_dynamic(body)
