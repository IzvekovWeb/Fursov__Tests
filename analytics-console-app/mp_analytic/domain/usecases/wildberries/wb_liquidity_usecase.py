import datetime

from config.constants import WB_TOKEN
from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_abc import ABCReport
from data.repository.wildberries.wb_dynamic_orders import DynamicOrdersReport
from data.repository.wildberries.wb_liquidity import LiquidityReport
from data.repository.wildberries.wb_profitability import ProfitabilityReport
from data.repository.wildberries.wb_report_stocks import StocksReport


class LiquidityUseCase:
    def __init__(self):
        self.urls = []

    def execute(self):
        sheet_title_prices = SHEETS.get('prices').get('title')
        sheet_id_prices = SHEETS.get('prices').get('id')

        prices = self.price_formatting(
            GoogleSheetAPI(sheet_title_prices, SPREADSHEET_ID_SECOND, sheet_id_prices).get_column('A', 'B'))
        profitability = ProfitabilityReport(WB_TOKEN, prices, weeks=2).execute()[0][1:]
        dynamic = DynamicOrdersReport().execute()[1][1:]
        date_from = datetime.date.today() - datetime.timedelta(7)
        date_to = datetime.date.today()
        stocks = StocksReport(date_to=date_to.strftime('%Y-%m-%d'),
                              date_from=date_from.strftime('%Y-%m-%d')).execute()[1:]
        abc = ABCReport().execute(profitability, dynamic, stocks)

        response = LiquidityReport().execute(abc)
        sheet_title = SHEETS.get('liquidity').get('title')
        sheet_id = SHEETS.get('liquidity').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)
        table.clear()
        table.insert(response)

        return True

    def price_formatting(self, price):
        return {price[0][i]: int(price[1][i]) if price[1][i] else '-' for i in range(1, len(price[0]))}


if __name__ == '__main__':
    LiquidityUseCase().execute()
