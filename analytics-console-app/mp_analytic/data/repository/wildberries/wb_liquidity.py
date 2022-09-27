import datetime

from config.constants import WB_TOKEN
from config.sheets import SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_abc import ABCReport
from data.repository.wildberries.wb_dynamic_orders import DynamicOrdersReport
from data.repository.wildberries.wb_profitability import ProfitabilityReport
from data.repository.wildberries.wb_report_stocks import StocksReport
from data.utils.functions import price_formatting


class LiquidityReport:
    def __init__(self):
        self.abc = None
        self.profit_turnover = {'до 10': {'days': 0, 'count': 0},
                                'от 10 до 20': {'days': 0, 'count': 0},
                                'от 20 до 30': {'days': 0, 'count': 0},
                                'от 30 до 40': {'days': 0, 'count': 0},
                                '40+': {'days': 0, 'count': 0}
                                }
        self.liq_stocks = {'отлично (до 7 дней)': 0,
                           'хорошо (7-30 дней)': 0,
                           'средне (30-60 дней)': 0,
                           'плохо (60+ дней)': 0}

        self.profit_stocks = {'до 10': 0,
                              'от 10 до 20': 0,
                              'от 20 до 30': 0,
                              'от 30 до 40': 0,
                              '40+': 0}

        self.liq_profit = {'отлично (до 7 дней)': {'profit': 0, 'count': 0},
                           'хорошо (7-30 дней)': {'profit': 0, 'count': 0},
                           'средне (30-60 дней)': {'profit': 0, 'count': 0},
                           'плохо (60+ дней)': {'profit': 0, 'count': 0}}

    def execute(self, abc):
        self.abc = abc
        self.get_data()
        return self.__get_table()

    def get_data(self):
        self.__get_profit_turnover()
        self.__get_profit_stocks()
        self.__get_liq_stocks()
        self.__get_liq_profit()

    def __get_profit_turnover(self):

        for row in self.abc:
            profit = row[9]
            days = row[11]

            if type(profit) != str and type(days) != str:
                self.profit_turnover[get_category_profit(profit)]['days'] += days
                self.profit_turnover[get_category_profit(profit)]['count'] += 1

        for key, value in self.profit_turnover.items():
            self.profit_turnover[key] = round(value['days'] / value['count'] if value['count'] else 0, 2)

    def __get_profit_stocks(self):
        sum = 0
        for row in self.abc:
            profit = row[9]
            price = row[3]
            stocks = row[8]

            if type(stocks) != str and type(profit) != str and type(price) != str:
                sum += stocks * price
                self.profit_stocks[get_category_profit(profit)] += stocks * price

        for key, value in self.profit_stocks.items():
            self.profit_stocks[key] = round(value / sum * 100, 2)

    def __get_liq_stocks(self):
        sum = 0
        for row in self.abc:
            turnover = row[11]
            price = row[3]
            stocks = row[8]

            if type(stocks) != str and type(turnover) != str and type(price) != str:
                sum += stocks * price
                self.liq_stocks[get_category_turnover(turnover)] += stocks * price

        for key, value in self.liq_stocks.items():
            self.liq_stocks[key] = round(value / sum * 100, 2)

    def __get_liq_profit(self):
        for row in self.abc:
            turnover = row[11]
            profit = row[9]

            if type(turnover) != str and type(profit) != str:
                self.liq_profit[get_category_turnover(turnover)]['profit'] += profit
                self.liq_profit[get_category_turnover(turnover)]['count'] += 1

        for key, value in self.liq_profit.items():
            self.liq_profit[key] = round(value['profit'] / value['count'], 2)

    def __get_table(self):
        table = []
        t = [["Категория рентабельности, %", "Оборачиваемость, дни"],
             ['до 10'],
             ['от 10 до 20'],
             ['от 20 до 30'],
             ['от 30 до 40'],
             ['40+']]
        for i in range(1, len(t)):
            t[i].append(self.profit_turnover[t[i][0]])
        table.extend(t)
        table.append([''])
        table.append([''])
        t = [["Категория рентабельности, %", "Процент остатков, руб"],
             ['до 10'],
             ['от 10 до 20'],
             ['от 20 до 30'],
             ['от 30 до 40'],
             ['40+']]
        for i in range(1, len(t)):
            t[i].append(self.profit_stocks[t[i][0]])
        table.extend(t)

        table.append([''])
        table.append([''])
        t = [["Категория ликвидности, дни", "Процент остатоков, руб"],
             ['отлично (до 7 дней)'],
             ['хорошо (7-30 дней)'],
             ['средне (30-60 дней)'],
             ['плохо (60+ дней)'], ]
        for i in range(1, len(t)):
            t[i].append(self.liq_stocks[t[i][0]])
        table.extend(t)
        table.append([''])
        table.append([''])
        t = [["Категория ликвидности, дни", "Рентабельность, %"],
             ['отлично (до 7 дней)'],
             ['хорошо (7-30 дней)'],
             ['средне (30-60 дней)'],
             ['плохо (60+ дней)'], ]
        for i in range(1, len(t)):
            t[i].append(self.liq_profit[t[i][0]])
        table.extend(t)
        return table


def get_category_profit(value):
    if value < 10:
        return 'до 10'
    elif 10 <= value < 20:
        return 'от 10 до 20'
    elif 20 <= value < 30:
        return 'от 20 до 30'
    elif 30 <= value < 40:
        return 'от 30 до 40'
    elif 40 <= value:
        return '40+'


def get_category_turnover(value):
    if value < 7:
        return 'отлично (до 7 дней)'
    elif 7 <= value < 30:
        return 'хорошо (7-30 дней)'
    elif 30 <= value < 60:
        return 'средне (30-60 дней)'
    elif 60 <= value:
        return 'плохо (60+ дней)'


if __name__ == '__main__':
    prices = price_formatting(
        GoogleSheetAPI("себес", SPREADSHEET_ID_SECOND, "1896206900").get_column('A', 'B'))
    profitability = ProfitabilityReport(WB_TOKEN, prices, weeks=2).execute()[0][1:]
    dynamic = DynamicOrdersReport().execute()[1][1:]
    date_from = datetime.date.today() - datetime.timedelta(7)
    date_to = datetime.date.today()
    stocks = StocksReport(date_to=date_to.strftime('%Y-%m-%d'),
                          date_from=date_from.strftime('%Y-%m-%d')).execute()[1:]
    abc = ABCReport().execute(profitability, dynamic, stocks)[1:]
    response = LiquidityReport().execute(abc)
