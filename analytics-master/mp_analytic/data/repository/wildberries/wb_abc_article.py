from data.utils.abc_utils import get_row_for_abc


class ABCArticleReport:
    def __init__(self):
        self.response = {}

    def execute(self, profitability, dynamic, stocks):
        self.__get_profitability(profitability)
        self.__get_turnover(dynamic, stocks)
        return self.__get_table()

    def __get_profitability(self, profitability):
        for row in profitability:
            subject, article, rub, op = row[2], row[4], row[6], row[10]

            if self.response.get(article):
                if not isinstance(self.response[article].get('op'), str) and not isinstance(op, str):
                    self.response[article]['op'] += op
                elif isinstance(self.response[article].get('op'), str) and not isinstance(op, str):
                    self.response[article]['op'] = op
                self.response[article]['rub'] += rub
            else:
                self.response[article] = {'subject': subject, 'article': article, 'op': op, 'rub': rub, 'dynamic': '-',
                                          'stocks': '-'}

    def __get_turnover(self, dynamic, stocks):
        for row in dynamic:
            article = row[4]
            if self.response.get(article):
                if not isinstance(self.response[article].get('dynamic'), str):
                    self.response[article]['dynamic'] += row[-1]
                else:
                    self.response[article]['dynamic'] = row[-1]
            else:
                self.response[article] = {'subject': row[2], 'article': article, 'op': '-', 'rub': '-',
                                          'dynamic': row[-1], 'stocks': '-'}

        for row in stocks:
            article = row[3]
            if self.response.get(article):
                if not isinstance(self.response[article].get('stocks'), str):
                    self.response[article]['stocks'] += row[-1]
                else:
                    self.response[article]['stocks'] = row[-1]
            else:
                self.response[article] = {'subject': '-', 'article': article, 'op': '-', 'rub': '-',
                                          'dynamic': '-', 'stocks': row[-1]}

    def __get_table(self):
        table = [["Предмет", "Артикул", "Рентабельность", "Оборачиваемость", "Итог"]]

        for article in self.response.values():
            profit_letter, turnover_letter, abc = get_row_for_abc(article.get('op'), article.get('rub'),
                                                                  article.get('dynamic'), article.get('stocks'))
            table.append([article['subject'], article['article'], profit_letter, turnover_letter, abc])
        return table
