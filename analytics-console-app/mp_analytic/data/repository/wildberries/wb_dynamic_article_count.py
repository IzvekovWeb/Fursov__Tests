import datetime

from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.utils.functions import form_days, date_to_point_format
from domain.utils.functions import get_suppliers_list


class DynamicArticleCountReport:
    """
    Динамика по артикулам (шт)
    """

    def __init__(self, wb_token, suppliers=None, date_from=None, date_to=None, flag=1):
        self.__wb_token = wb_token
        self.__suppliers = get_suppliers_list() if suppliers is None else get_suppliers_list(suppliers)
        self.flag = flag
        if date_from is None and date_to is None:
            if not flag:
                date_to = datetime.date.today() - datetime.timedelta(1)
                date_from = date_to - datetime.timedelta(6)
                self.days = form_days(7, dot_format=1)
            else:
                date_to = datetime.date.today()
                date_from = date_to - datetime.timedelta(7)
                self.days = form_days(7, dot_format=1, flag_today=0)

        self.date_from = date_to_point_format(date_from.strftime("%Y-%m-%d"))
        self.date_to = date_to_point_format(date_to.strftime("%Y-%m-%d"))
        self.response = {}

    def execute(self):
        print('===== ОТЧЕТ "ДИНАМИКА ПО АРТ (ШТ)" =====')
        for supplier in self.__suppliers:
            print(f"\rОбрабатываем - {supplier.get('name')}")
            self.__get_nomenclatures(supplier.get('supplier-id'), supplier.get('name'))
            self.__get_data(supplier.get('supplier-id'), supplier.get('name'))
        return self.__get_table()

    def __get_nomenclatures(self, supplier_id: str, supplier_name: str):
        """
        Сбор номенклатур
        :param supplier_id: id поставщика
        :param supplier_name: имя поставщика
        :return:
        """
        data = PersonalAccountAPI.get_nomenclatures(supplier_id)
        for nomenclature in data:
            article = nomenclature['sa'].split('/')[0]
            if not self.response.get(article + supplier_name):
                self.response[article + supplier_name] = {'supplier': supplier_name,
                                                          'article': article,
                                                          'nm_id': nomenclature['nmID'],
                                                          'brand': nomenclature['brandName'],
                                                          'subject': nomenclature['subjectName'], 'days': {}}

    def __get_data(self, supplier_id: str, supplier_name: str):
        """
        Сбор
        :param supplier_id: id поставщика
        :param supplier_name: имя поставщика
        :return:
        """
        response = PersonalAccountAPI.get_dynamic(supplier_id, self.date_from, self.date_to)
        data = response[0]['data']['weeklyTables']

        for brand in data:  # brands data
            brand_name = brand['brand']
            for week in brand['weeks']:  # week data
                for day in week['days']:  # days data
                    date = day['day']
                    for orders in day['articles']:  # articles data
                        article = orders['article'].split('/')[0]  # get pure article
                        pieces = orders['orderGoodsPiece']  # get orders count

                        if self.response.get(article + supplier_name):
                            if self.response.get(article + supplier_name)['days'].get(date):
                                self.response[article + supplier_name]['days'][date] += pieces
                            else:
                                self.response[article + supplier_name]['days'][date] = pieces
                        else:
                            self.response[article + supplier_name] = {'supplier': supplier_name, 'brand': brand_name,
                                                                      'nm_id': '-',
                                                                      'subject': '-', 'article': article,
                                                                      'days': {date: pieces}}

    def __get_table(self) -> list:
        """
        Формирование таблицы
        :return: list
        """
        table = [
            ["Поставщик", "Бренд", "Предмет", "Номенклатура", "Артикул", *self.days, 'Итого']]
        for article in self.response.values():
            days_sum = 0
            row = [article['supplier'], article['brand'], article['subject'], article['nm_id'], article['article']]
            iter_days = self.days[:-1] if self.flag else self.days
            for day in iter_days:
                pieces = article['days'].get(day)
                if pieces:
                    days_sum += pieces
                    row.append(pieces)
                else:
                    row.append(0)
            if self.flag:
                row.append(article['days'].get(self.days[-1]) if article['days'].get(self.days[-1]) else 0)
            row.append(days_sum)
            table.append(row)
        return table
