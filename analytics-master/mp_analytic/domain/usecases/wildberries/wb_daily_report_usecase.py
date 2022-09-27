from config.color_constants import *
from data.google.get_body_methods.get_body import *
from data.google.get_range_methods.get_range import get_range_colorize
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_daily_report import DailyReport
from data.utils.functions import update_at


class DailyReportUseCase:
    """
    Ежедневный отчет
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.update_at = None
        self.dashboard_data = None

    def execute(self, days_count=7):
        suppliers = self.kwargs.get("suppliers")
        report = DailyReport(days_count, suppliers)
        response = report.execute()

        spreadsheet_id = self.kwargs.get("Wildberries")
        sheet_title = "День"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()
        table.clear_cond()
        table.insert(response)

        self.clear_color(table)
        self.design(table, sheet_id)

        self.update_at = update_at(response)

        self.dashboard_data = report.get_drf_stat()

        return self.update_at

    def design(self, table, sheet_id):
        _range = get_range_colorize
        _body = get_body_colorize
        body = {"requests": []}
        _body(body, _range(0, 1, 0, 8, sheet_id), BLUE_LIGHT)
        _body(body, _range(9, 10, 0, 8, sheet_id), BLUE_LIGHT)
        table.colorize_row(body)

        table.conditional_color_format(12, 14)

        table.number_format(1, 11, 1, 7)
        table.percent_format(1, 11, 7, 8)
        table.percent_format(12, 14, 1, 8)

    def clear_color(self, table):
        table.colorize_row()
