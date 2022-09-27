import datetime

from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_abc import ABCReport
from data.repository.wildberries.wb_dynamic_orders import DynamicOrdersReport
from data.repository.wildberries.wb_liquidity import LiquidityReport
from data.repository.wildberries.wb_profitability import ProfitabilityReport
from data.repository.wildberries.wb_report_stocks import StocksReport
from data.utils.functions import update_at
from domain.utils.functions import price_formatting


class LiquidityUseCase:
    """
    Ликвидность
    """

    def __init__(self, kwargs: dict):
        self.dashboard_data = {}
        self.kwargs = kwargs

        self.update_at = None

    def execute(self):
        suppliers = self.kwargs.get("suppliers")
        spreadsheet_id_prices = self.kwargs.get("Wildberries Log PC")
        sheet_title_prices = "Себестоимость"
        sheet_id_prices = self.kwargs.get(sheet_title_prices)

        prices = price_formatting(
            GoogleSheetAPI(sheet_title_prices, spreadsheet_id_prices, sheet_id_prices).get_column('A', 'B')
        )

        profitability = ProfitabilityReport(prices, suppliers=suppliers).execute()[0][1:]
        dynamic = DynamicOrdersReport(suppliers=suppliers).execute()[1][1:]

        date_from = datetime.date.today() - datetime.timedelta(7)
        date_to = datetime.date.today()

        stocks = StocksReport(date_to=date_to.strftime('%Y-%m-%d'),
                              date_from=date_from.strftime('%Y-%m-%d'),
                              suppliers=suppliers
                              ).execute()[1:]
        abc = ABCReport().execute(profitability, dynamic, stocks)

        response = LiquidityReport().execute(abc)

        spreadsheet_id = self.kwargs.get("Wildberries 2")
        sheet_title = "Ликвидность"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()
        table.insert(response)

        self.update_at = update_at(response, table.insert)

        self.__collect_data(response)

        return self.update_at

    def __collect_data(self, response):
        self.dashboard_data["rent_days"] = {"data": [], "values": []}
        self.dashboard_data["rent_remains"] = {"data": [], "values": []}
        self.dashboard_data["liquid_remains"] = {"data": [], "values": []}
        self.dashboard_data["liquid_rent"] = {"data": [], "values": []}

        for i in range(1, 6):
            self.dashboard_data["rent_days"]["data"].append(response[i][0])
            self.dashboard_data["rent_days"]["values"].append(response[i][1])

        for i in range(9, 14):
            self.dashboard_data["rent_remains"]["data"].append(response[i][0])
            self.dashboard_data["rent_remains"]["values"].append(response[i][1])

        for i in range(17, 21):
            self.dashboard_data["liquid_remains"]["data"].append(response[i][0])
            self.dashboard_data["liquid_remains"]["values"].append(response[i][1])

        for i in range(24, 28):
            self.dashboard_data["liquid_rent"]["data"].append(response[i][0])
            self.dashboard_data["liquid_rent"]["values"].append(response[i][1])
