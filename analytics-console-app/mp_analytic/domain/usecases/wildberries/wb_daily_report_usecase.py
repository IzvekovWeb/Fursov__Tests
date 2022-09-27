from config.constants import WB_TOKEN
from config.sheets import SHEETS, SPREADSHEET_ID
from config.color_constants import *
from data.google.get_body_methods.get_body import *
from data.google.get_range_methods.get_range import get_range_colorize
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_daily_report import DailyReport


class DailyReportUseCase:
    """
    Отчет "День"
    """

    def __init__(self):
        sheet_title = SHEETS.get('day').get('title')
        self.sheet_id = SHEETS.get('day').get('id')

        self.__table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID, self.sheet_id)

        self.drf_stat = None

    def execute(self, days_count=7):
        report = DailyReport(days_count, WB_TOKEN)
        response = report.execute()

        self.__table.clear()
        self.__table.clear_cond()
        self.__table.insert(response)

        self.clear_color()
        self.design()

        self.drf_stat = report.get_drf_stat()

        return self.__table.get_sheet_url()

    def design(self):
        _range = get_range_colorize
        _body = get_body_colorize
        body = {"requests": []}
        _body(body, _range(0, 1, 0, 8, self.sheet_id), BLUE_LIGHT)
        _body(body, _range(9, 10, 0, 8, self.sheet_id), BLUE_LIGHT)
        self.__table.colorize_row(body)

        self.__table.conditional_color_format(12, 14)

        self.__table.number_format(1, 11, 1, 7)
        self.__table.percent_format(1, 11, 7, 8)
        self.__table.percent_format(12, 14, 1, 8)

    def clear_color(self):
        self.__table.colorize_row()
