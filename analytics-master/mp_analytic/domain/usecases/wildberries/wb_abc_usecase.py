import datetime

from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_abc import ABCReport
from data.repository.wildberries.wb_abc_article import ABCArticleReport
from data.repository.wildberries.wb_abc_subject import ABCSubjectReport
from data.repository.wildberries.wb_dynamic_orders import DynamicOrdersReport
from data.repository.wildberries.wb_profitability import ProfitabilityReport
from data.repository.wildberries.wb_report_stocks import StocksReport
from data.utils.functions import update_at
from domain.utils.functions import price_formatting


class ABCUseCase:
    def __init__(self, kwargs: dict):
        self.update_at = None
        self.profitability = None
        self.dynamic = None
        self.stocks = None
        self.urls = []

        self.kwargs = kwargs
        self.dashboard_data = None

    def execute(self):
        suppliers = self.kwargs.get("suppliers")
        spreadsheet_id_logistics = self.kwargs.get("Wildberries Log PC")
        sheet_title_prices = "Себестоимость"
        sheet_id_prices = self.kwargs.get(sheet_title_prices)

        prices = price_formatting(
            GoogleSheetAPI(sheet_title_prices, spreadsheet_id_logistics, sheet_id_prices).get_column('A', 'B'))
        self.profitability = ProfitabilityReport(prices, suppliers=suppliers).execute()[0][1:]
        self.dynamic = DynamicOrdersReport(suppliers=suppliers).execute()[1][1:]

        date_from = datetime.date.today() - datetime.timedelta(7)
        date_to = datetime.date.today()
        self.stocks = StocksReport(date_to=date_to.strftime('%Y-%m-%d'),
                                   date_from=date_from.strftime('%Y-%m-%d'),
                                   suppliers=suppliers).execute()[1:]

        self.abc_title()
        self.abc_article()
        response = self.abc_subject()

        self.update_at = update_at(response)

        return self.update_at

    def abc_title(self):
        report = ABCReport()
        response = report.execute(self.profitability, self.dynamic, self.stocks)
        spreadsheet_id = self.kwargs.get("Wildberries 2")
        sheet_title = "ABC"
        sheet_id = self.kwargs.get(sheet_title)

        self.dashboard_data = report.get_drf_data()

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)
        table.clear()
        table.insert(response)

    def abc_article(self):
        response = ABCArticleReport().execute(self.profitability, self.dynamic, self.stocks)
        spreadsheet_id = self.kwargs.get("Wildberries 2")
        sheet_title = "ABC (арт)"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()
        table.insert(response)

    def abc_subject(self):
        response = ABCSubjectReport().execute(self.profitability, self.dynamic, self.stocks)
        spreadsheet_id = self.kwargs.get("Wildberries 2")
        sheet_title = "ABC (предмет)"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()
        table.insert(response)
        return response
