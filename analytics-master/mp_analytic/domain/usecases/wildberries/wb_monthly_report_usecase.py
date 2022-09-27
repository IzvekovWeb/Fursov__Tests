import datetime

from config.color_constants import *
from data.google.get_body_methods.get_body import *
from data.google.get_range_methods.get_range import get_range_colorize
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_monthly_report import MonthlyReport
from data.utils.functions import update_at
from domain.utils.wb_drf_data_weekly_monthly import get_drf_data


class MonthlyReportUseCase:
    """
    Ежедневный отчет за месяц
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.__days_count = (datetime.datetime.today() - datetime.timedelta(1)).day
        self.update_at = None
        self.dashboard_data = None

    def execute(self):
        suppliers = self.kwargs.get("suppliers")
        spreadsheet_id = self.kwargs.get("Wildberries")

        sheet_title_plan = "План"
        sheet_id_plan = self.kwargs.get(sheet_title_plan)

        row = GoogleSheetAPI(sheet_title_plan, spreadsheet_id, sheet_id_plan).get_row(4)[0]

        plan = [int(i) for i in row]

        response = MonthlyReport(self.__days_count, suppliers).execute(plan)

        sheet_title = "Месяц"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        self.__days_count = len(response) - 14

        table.clear()
        table.clear_cond()
        self.clear_color(table)

        table.insert(response)
        self.design_table(table, sheet_id)

        self.update_at = update_at(response)

        self.dashboard_data = get_drf_data(response)

        return self.update_at

    def design_table(self, table, table_id):
        _range = get_range_colorize
        _body = get_body_colorize

        body = {"requests": []}

        _body(body=body, _range=_range(0, 1, 0, 8, table_id), _color=BLUE_LIGHT)
        _body(body, _range(self.__days_count + 1, self.__days_count + 2, 0, 8, table_id), BLUE_LIGHT)

        table.conditional_color_format(self.__days_count + 3, self.__days_count + 5)

        _body(body, _range(self.__days_count + 6, self.__days_count + 7, 0, 8, table_id), SKIN_LIGHT)
        _body(body, _range(self.__days_count + 7, self.__days_count + 8, 0, 8, table_id), PURPLE_LIGHT)
        _body(body, _range(self.__days_count + 8, self.__days_count + 9, 0, 8, table_id), PINK_LIGHT)
        _body(body, _range(self.__days_count + 9, self.__days_count + 10, 0, 8, table_id), PURPLE_LIGHT)
        _body(body, _range(self.__days_count + 10, self.__days_count + 11, 0, 8, table_id), SKIN)
        _body(body, _range(self.__days_count + 11, self.__days_count + 12, 0, 8, table_id), SKIN_LIGHT)
        _body(body, _range(self.__days_count + 12, self.__days_count + 13, 0, 8, table_id), SALAD)
        _body(body, _range(self.__days_count + 13, self.__days_count + 14, 0, 8, table_id), SKIN_SUPER_LIGHT)
        table.colorize_row(body)

        table.number_format(1, self.__days_count + 2, 1, 7)
        table.number_format(self.__days_count + 8, self.__days_count + 9, 1, 7)
        table.number_format(self.__days_count + 11, self.__days_count + 13, 1, 7)

        table.percent_format(1, self.__days_count + 10, 7, 8)
        table.percent_format(self.__days_count + 3, self.__days_count + 5, 1, 8)
        table.percent_format(self.__days_count + 9, self.__days_count + 11, 1, 8)
        table.percent_format(self.__days_count + 13, self.__days_count + 14, 1, 8)

    def clear_color(self, table):
        table.colorize_row()
