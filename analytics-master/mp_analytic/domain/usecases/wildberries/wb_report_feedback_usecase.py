from data.google.get_body_methods.get_body import get_body_feedbacks
from data.google.get_range_methods.get_range import get_range_feedbacks
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_report_feedback import FeedbackReport
from data.utils.functions import update_at


class FeedbackReportUseCase:
    """
    Отчет "Отзывы"
    """
    
    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.update_at = None

    def execute(self) -> str:
        suppliers = self.kwargs.get("suppliers")
        response = FeedbackReport(suppliers=suppliers).execute()

        spreadsheet_id = self.kwargs.get("Wildberries 2")
        sheet_title = "Отзывы"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()
        table.insert(response)

        self.clear_red_text(table)
        self.google_sheets_operate(table, response)

        self.update_at = update_at(response, table.insert)

        return self.update_at

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
