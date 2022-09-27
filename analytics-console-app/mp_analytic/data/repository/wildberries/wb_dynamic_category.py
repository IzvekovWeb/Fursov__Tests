import datetime

from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.utils.functions import form_days, date_to_point_format
from domain.utils.functions import get_suppliers_list


class DynamicCategoryReport:
    """
    Динамика "Категории"
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
        self.categories = {}
        self.__drf_orders = []

    def execute(self) -> list:
        print('====== ДИНАМИКА ПО КАТЕГОРИЯМ ======')
        for supplier in self.__suppliers:
            print(f"\rОбрабатываем - {supplier.get('name')}")
            self.__get_nomenclatures(supplier['supplier-id'])
            self.get_data(supplier['supplier-id'])
        return self.__get_table()

    def __get_nomenclatures(self, supplier_id):
        """
        Получение списка номенклатур
        :param supplier_id: id поставщика
        :return:
        """
        data = PersonalAccountAPI.get_nomenclatures(supplier_id)
        for nm in data:
            if not self.response.get(nm['sa']):
                self.response[nm['sa']] = {'article': nm['sa'], 'subject': nm['subjectName'], 'days': {}}

    def get_data(self, supplier_id):
        """
        Формирование данных
        :param supplier_id: id поставщика
        :return:
        """
        response = PersonalAccountAPI.get_dynamic(supplier_id, self.date_from, self.date_to)
        data = response[0]['data']['weeklyTables']

        for brand in data:
            for week in brand['weeks']:
                for day in week['days']:
                    date = day['day']
                    for orders in day['articles']:
                        price = round(orders['costPrice'] / 85 * 100)

                        nm = self.response.get(orders['article'])
                        if nm:  # Если номенклатура есть в словаре
                            subject = nm['subject']
                            if self.categories.get(subject):  # Если категория номенклатуры есть в словаре
                                if self.categories[subject]['days'].get(date):
                                    self.categories[subject]['days'][date] += price
                                else:
                                    self.categories[subject]['days'][date] = price
                            else:
                                self.categories[subject] = {'subject': subject, 'days': {date: price}}

    def __get_table(self) -> list:
        """
        Формирование таблицы
        :return: list
        """
        table = [["Категория", *self.days, 'Итого']]
        top_dict = []

        for article in self.categories.values():
            days_sum = 0
            row = [article['subject']]

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

            top_dict.append((len(table) - 1, days_sum))

        self.__collect_top_orders(table, top_dict)

        return table

    def __collect_top_orders(self, table: list, top_dict: list):

        top_dict.sort(key=lambda tup: tup[1], reverse=True)

        if len(top_dict) < 10:
            top_count = len(top_dict)
        else:
            top_count = 10

        for idx in range(top_count):
            row = table[top_dict[idx][0]]

            self.__drf_orders.append({
                "ordersAmount": row[-1],
                "subject": row[0],
            })

    def get_drf_orders(self):
        return self.__drf_orders
