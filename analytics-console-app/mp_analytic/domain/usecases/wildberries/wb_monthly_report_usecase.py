import datetime

from config.constants import WB_TOKEN
from config.color_constants import *
from data.google.get_body_methods.get_body import *
from config.sheets import SHEETS, SPREADSHEET_ID
from data.google.get_range_methods.get_range import get_range_colorize
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_monthly_report import MonthlyReport


class MonthlyReportUseCase:
    """
        Отчет "Месяц"
        """

    def __init__(self):

        sheet_title = SHEETS.get('month').get('title')
        self.__table_id = SHEETS.get('month').get('id')
        self.__days_count = (datetime.datetime.today() - datetime.timedelta(1)).day
        self.__table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID, self.__table_id)

    def execute(self):
        sheet_title_plan = SHEETS.get('plan').get('title')
        sheet_id_plan = SHEETS.get('plan').get('id')

        row = GoogleSheetAPI(sheet_title_plan, SPREADSHEET_ID, sheet_id_plan).get_row(4)[0]
        plan = [int(i) for i in row]
        response = MonthlyReport(WB_TOKEN, self.__days_count).execute(plan)
        self.__days_count = len(response) - 14
        self.__table.clear()
        self.__table.clear_cond()
        self.__table.colorize_row()
        self.__table.insert(response)
        self.design_table()

        return self.__table.get_sheet_url()

    def design_table(self):
        _range = get_range_colorize
        _body = get_body_colorize
        body = {"requests": []}
        _body(body=body, _range=_range(0, 1, 0, 8, self.__table_id), _color=BLUE_LIGHT)
        _body(body, _range(self.__days_count + 1, self.__days_count + 2, 0, 8, self.__table_id), BLUE_LIGHT)

        self.__table.conditional_color_format(self.__days_count + 3, self.__days_count + 5)

        _body(body, _range(self.__days_count + 6, self.__days_count + 7, 0, 8, self.__table_id), SKIN_LIGHT)
        _body(body, _range(self.__days_count + 7, self.__days_count + 8, 0, 8, self.__table_id), PURPLE_LIGHT)
        _body(body, _range(self.__days_count + 8, self.__days_count + 9, 0, 8, self.__table_id), PINK_LIGHT)
        _body(body, _range(self.__days_count + 9, self.__days_count + 10, 0, 8, self.__table_id), PURPLE_LIGHT)
        _body(body, _range(self.__days_count + 10, self.__days_count + 11, 0, 8, self.__table_id), SKIN)
        _body(body, _range(self.__days_count + 11, self.__days_count + 12, 0, 8, self.__table_id), SKIN_LIGHT)
        _body(body, _range(self.__days_count + 12, self.__days_count + 13, 0, 8, self.__table_id), SALAD)
        _body(body, _range(self.__days_count + 13, self.__days_count + 14, 0, 8, self.__table_id), SKIN_SUPER_LIGHT)
        self.__table.colorize_row(body)

        self.__table.number_format(1, self.__days_count + 2, 1, 7)
        self.__table.number_format(self.__days_count + 8, self.__days_count + 9, 1, 7)
        self.__table.number_format(self.__days_count + 11, self.__days_count + 13, 1, 7)

        self.__table.percent_format(1, self.__days_count + 10, 7, 8)
        self.__table.percent_format(self.__days_count + 3, self.__days_count + 5, 1, 8)
        self.__table.percent_format(self.__days_count + 9, self.__days_count + 11, 1, 8)
        self.__table.percent_format(self.__days_count + 13, self.__days_count + 14, 1, 8)

    def clear_color(self):
        self.__table.colorize_row()
