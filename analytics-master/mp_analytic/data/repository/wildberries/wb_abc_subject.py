from data.utils.abc_utils import get_row_for_abc


class ABCSubjectReport:
    def __init__(self):
        self.__response = {}

    def execute(self, profitability, dynamic, stocks):
        self.__get_profitability(profitability)
        self.__get_turnover(dynamic, stocks)
        self.__subject_group()
        return self.__get_table()

    def __get_profitability(self, profitability):
        for row in profitability:
            op = row[10]
            rub = row[6]

            article = row[4]
            if self.__response.get(article):
                if type(op) != str and type(self.__response[article]['op']) != str:
                    self.__response[article]['op'] += op
                elif type(self.__response[article]['op']) == str and type(op) != str:
                    self.__response[article]['op'] = op
                self.__response[article]['rub'] += rub
            else:
                self.__response[article] = {'subject': row[2], 'article': article, 'op': op, 'rub': rub, 'dynamic': '-',
                                          'stocks': '-'}

    def __get_turnover(self, dynamic, stocks):
        for row in dynamic:
            article = row[4]
            if self.__response.get(article):
                if type(self.__response[article]['dynamic']) != str:
                    self.__response[article]['dynamic'] += row[-1]
                else:
                    self.__response[article]['dynamic'] = row[-1]
            else:
                self.__response[article] = {'subject': row[2], 'article': article, 'op': '-', 'rub': '-',
                                          'dynamic': row[-1], 'stocks': '-'}

        for row in stocks:
            article = row[3]
            if self.__response.get(article):
                if type(self.__response[article]['stocks']) != str:
                    self.__response[article]['stocks'] += row[-1]
                else:
                    self.__response[article]['stocks'] = row[-1]
            else:
                self.__response[article] = {'subject': '-', 'article': article, 'op': '-', 'rub': '-',
                                          'dynamic': '-', 'stocks': row[-1]}

    def __subject_group(self):
        sub_dict = {}
        for article in self.__response.values():
            if sub_dict.get(article.get('subject')):
                sub_dict_article_subject = sub_dict[article['subject']]
                op = article.get('op')
                rub = article.get('rub')
                dynamic = article.get('dynamic')
                stocks = article.get('stocks')

                if not isinstance(op, str) and not isinstance(sub_dict_article_subject.get('op'), str):
                    sub_dict[article['subject']]['op'] += op
                elif isinstance(sub_dict_article_subject['op'], str) and not isinstance(op, str):
                    sub_dict[article['subject']]['op'] = op

                if not isinstance(rub, str) and not isinstance(sub_dict_article_subject['rub'], str):
                    sub_dict[article['subject']]['rub'] += rub
                elif isinstance(sub_dict_article_subject['rub'], str) and not isinstance(rub, str):
                    sub_dict[article['subject']]['op'] = rub

                if not isinstance(sub_dict_article_subject['dynamic'], str) and not isinstance(dynamic, str):
                    sub_dict[article['subject']]['dynamic'] += dynamic
                elif isinstance(sub_dict_article_subject['dynamic'], str) and not isinstance(dynamic, str):
                    sub_dict[article['subject']]['dynamic'] = dynamic

                if type(sub_dict_article_subject['stocks']) != str and not isinstance(stocks, str):
                    sub_dict[article['subject']]['stocks'] += stocks
                elif not isinstance(stocks, str):
                    sub_dict[article['subject']]['stocks'] = stocks
            else:
                sub_dict[article['subject']] = {'subject': article['subject'], 'op': article['op'],
                                                'rub': article['rub'], 'dynamic': article['dynamic'],
                                                'stocks': article['stocks']}
        self.__response = sub_dict

    def __get_table(self):
        table = [["Предмет", "Рентабельность", "Оборачиваемость", "Итог"]]

        for article in self.__response.values():
            profit_letter, turnover_letter, abc = get_row_for_abc(article.get('op'), article.get('rub'),
                                                                  article.get('dynamic'), article.get('stocks'))
            row = [article['subject'], profit_letter, turnover_letter, abc]
            table.append(row)
        return table
