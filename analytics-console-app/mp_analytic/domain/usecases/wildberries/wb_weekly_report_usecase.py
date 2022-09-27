import datetime

from config.constants import WB_TOKEN
from config.color_constants import *
from data.google.get_body_methods.get_body import *
from config.sheets import SHEETS, SPREADSHEET_ID
from data.google.get_range_methods.get_range import get_range_colorize
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_weekly_report import WeeklyReport


class WeeklyReportUseCase:
    """
    Отчет "Неделя"
    """

    def __init__(self):
        sheet_title = SHEETS.get('week').get('title')
        self.sheet_id = SHEETS.get('week').get('id')

        self.__table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID, self.sheet_id)

    def execute(self):
        sheet_title_plan = SHEETS.get('plan').get('title')
        sheet_id_plan = SHEETS.get('plan').get('id')

        row = GoogleSheetAPI(sheet_title_plan, SPREADSHEET_ID, sheet_id_plan).get_row(1)[0]
        plan = [int(i) for i in row]
        response = WeeklyReport(WB_TOKEN, datetime.datetime.today().isoweekday() - 1).execute(plan)
        self.__table.clear()
        self.__table.insert(response)
        self.clear_color()
        self.design_table()

        return self.__table.get_sheet_url()

    def design_table(self):
        _range = get_range_colorize
        _body = get_body_colorize
        body = {"requests": []}
        _body(body, _range(0, 1, 0, 8, self.sheet_id), BLUE_LIGHT)
        _body(body, _range(8, 9, 0, 8, self.sheet_id), BLUE_LIGHT)

        self.__table.conditional_color_format(10, 11)

        _body(body, _range(12, 13, 0, 8, self.sheet_id), SKIN_LIGHT)
        _body(body, _range(13, 14, 0, 8, self.sheet_id), PURPLE_LIGHT)
        _body(body, _range(14, 15, 0, 8, self.sheet_id), PINK_LIGHT)
        _body(body, _range(15, 16, 0, 8, self.sheet_id), PURPLE_LIGHT)
        _body(body, _range(16, 17, 0, 8, self.sheet_id), SKIN)
        _body(body, _range(17, 18, 0, 8, self.sheet_id), SKIN_LIGHT)
        _body(body, _range(18, 19, 0, 8, self.sheet_id), SALAD)
        _body(body, _range(19, 20, 0, 8, self.sheet_id), SKIN_SUPER_LIGHT)

        self.__table.colorize_row(body)

        self.__table.number_format(1, 10, 1, 7)
        self.__table.number_format(12, 15, 1, 7)
        self.__table.number_format(17, 19, 1, 7)

        self.__table.percent_format(1, 19, 7, 8)
        self.__table.percent_format(10, 12, 1, 8)
        self.__table.percent_format(15, 17, 1, 8)
        self.__table.percent_format(19, 20, 1, 8)

    def clear_color(self):
        self.__table.colorize_row()
