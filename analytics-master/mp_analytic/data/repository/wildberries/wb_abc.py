from data.utils.abc_utils import get_profit, get_turnover, get_abc


class ABCReport:
    def __init__(self):
        self.__drf_data = {}
        self.__response = {}

    def execute(self, profitability, dynamic, stocks):
        self.__get_profitability(profitability)
        self.__get_turnover(dynamic, stocks)
        return self.__get_table()

    def __get_profitability(self, profitability):
        """
        getting and forming profitability report
        """
        for row in profitability:
            op, sales, profit = row[10], row[6], '-'
            if not isinstance(op, str) and sales != 0:
                profit = abs(round(op / sales * 100))

            self.__response[row[4]] = {'subject': row[2], 'nm_id': row[3], 'article': row[4], 'profit': profit,
                                       'op': op, 'sales': sales, 'sales_count': row[5], 'price': row[9],
                                       'dynamic': '-', 'stocks': '-'}

    def __get_turnover(self, dynamic, stocks):
        """
        get and forming report of dynamic and stocks
        """
        for row in dynamic:
            article = row[4]
            if self.__response.get(article):
                self.__response[article]['dynamic'] = row[-1]
            else:
                self.__response[article] = {'subject': row[2], 'nm_id': row[3], 'op': '-', 'sales': '-', 'price': '-',
                                            'sales_count': '-', 'article': article, 'profit': '-', 'dynamic': row[-1],
                                            'stocks': '-'}

        for row in stocks:
            if self.__response.get(row[3]):
                self.__response[row[3]]['stocks'] = row[-1]

    def __get_table(self):
        table = [["Предмет", "Номенклатура", "Артикул/цвет", "Себестоимость", "ОП", "Продажи месяц (руб)",
                  "Продажи неделя (шт)", "Прибыль на 1 шт", "Остатки", "Рентабельность %", "Рентабельность",
                  "Оборачиваемость, дни", "Оборачиваемость", "Итог"]]
        self.drf()

        for article in self.__response.values():
            dynamic, profit, stocks, op, sales_count = article.get('dynamic'), article.get('profit'), \
                                                       article.get('stocks'), article.get('op'), \
                                                       article.get('sales_count')

            turnover = '-'
            if not isinstance(dynamic, str) and not isinstance(stocks, str):
                if dynamic != 0:
                    turnover = round(stocks / (dynamic / 7))
                    if not turnover: turnover = 1

            profit_letter = get_profit(profit) if not isinstance(profit, str) else '-'
            turnover_letter = get_turnover(turnover) if not isinstance(turnover, str) else '-'
            abc = get_abc(profit_letter, turnover_letter) if profit_letter != '-' and turnover_letter != '-' else '-'

            profit_one = '-'
            if not isinstance(op, str) and not isinstance(sales_count, str):
                profit_one = round(op / sales_count if sales_count != 0 else 0)
                if op < 0 and sales_count < 0:
                    profit_one *= -1

            row = [article.get('subject'), article.get('nm_id'), article.get('article'), article.get('price'), op,
                   article.get('sales'), dynamic, profit_one, stocks, profit, profit_letter, turnover, turnover_letter,
                   abc]
            table.append(row)

            self.__collect_drf_data(profit_letter, turnover_letter, abc)

        return table

    def drf(self):
        self.__drf_data = {
            "profit": {
                "data": ["A", "B", "C"],
                "values": [0, 0, 0]
            },
            "days": {
                "data": ["A", "B", "C"],
                "values": [0, 0, 0]
            },
            "abc": {
                "data": ["A", "B", "C"],
                "values": [0, 0, 0]
            }
        }

    def __collect_drf_data(self, profit, turnover, abc):
        if profit == "A":
            self.__drf_data["profit"]["values"][0] += 1
        elif profit == "B":
            self.__drf_data["profit"]["values"][1] += 1
        elif profit == "C":
            self.__drf_data["profit"]["values"][2] += 1

        if turnover == "A":
            self.__drf_data["days"]["values"][0] += 1
        elif turnover == "B":
            self.__drf_data["days"]["values"][1] += 1
        elif turnover == "C":
            self.__drf_data["days"]["values"][2] += 1

        if abc == "A":
            self.__drf_data["abc"]["values"][0] += 1
        elif abc == "B":
            self.__drf_data["abc"]["values"][1] += 1
        elif abc == "C":
            self.__drf_data["abc"]["values"][2] += 1

    def get_drf_data(self):
        return self.__drf_data
