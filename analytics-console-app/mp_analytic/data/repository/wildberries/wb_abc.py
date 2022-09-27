from data.utils.functions import get_profit, get_turnover, get_abc


class ABCReport:
    def __init__(self):
        self.response = {}

    def execute(self, profitability, dynamic, stocks):
        self.__get_profitability(profitability)
        self.__get_turnover(dynamic, stocks)
        return self.__get_table()

    def __get_profitability(self, profitability):
        for row in profitability:
            if type(row[10]) != str and row[6] != 0:
                profit = round(row[10] / row[6] * 100)
                if row[10] < 0 and row[6] < 0:
                    profit *= -1
            else:
                profit = '-'
            self.response[row[4]] = {'subject': row[2], 'nm_id': row[3], 'article': row[4], 'profit': profit,
                                     'op': row[10], 'sales': row[6], 'sales_count': row[5], 'price': row[9],
                                     'dynamic': '-', 'stocks': '-'}

    def __get_turnover(self, dynamic, stocks):
        for row in dynamic:
            if self.response.get(row[4]):
                self.response[row[4]]['dynamic'] = row[-1]
            else:
                self.response[row[4]] = {'subject': row[2], 'nm_id': row[3], 'op': '-', 'sales': '-', 'price': '-',
                                         'sales_count': '-', 'article': row[4], 'profit': '-', 'dynamic': row[-1],
                                         'stocks': '-'}

        for row in stocks:
            if self.response.get(row[3]):
                self.response[row[3]]['stocks'] = row[-1]

    def __get_table(self):
        table = [
            ["Предмет", "Номенклатура", "Артикул/цвет", "Себестоимость", "ОП", "Продажи месяц (руб)",
             "Продажи неделя (шт)", "Прибыль на 1 шт", "Остатки", "Рентабельность %", "Рентабельность",
             "Оборачиваемость, дни", "Оборачиваемость", "Итог"]]

        for article in self.response.values():
            profit_letter = get_profit(article['profit']) if article['profit'] != '-' else '-'

            turnover = '-'
            if article['dynamic'] != '-' and article['stocks'] != '-':
                if article['dynamic'] != 0:
                    turnover = round(article['stocks'] / (article['dynamic'] / 7))
                    if turnover == 0: turnover = 1

            turnover_letter = get_turnover(turnover) if turnover != '-' else '-'
            abc = '-'
            if profit_letter != '-' and turnover_letter != '-':
                abc = get_abc(profit_letter, turnover_letter)

            profit_one = '-'
            if type(article['op']) != str and type(article['sales_count']):
                profit_one = round(article['op'] / article['sales_count'] if article['sales_count'] != 0 else 0)
                if article['op'] < 0 and article['sales_count'] < 0:
                    profit_one *= -1

            row = [article['subject'], article['nm_id'], article['article'], article['price'], article['op'],
                   article['sales'], article['dynamic'], profit_one, article['stocks'],
                   article['profit'], profit_letter, turnover, turnover_letter, abc]
            table.append(row)
        return table
