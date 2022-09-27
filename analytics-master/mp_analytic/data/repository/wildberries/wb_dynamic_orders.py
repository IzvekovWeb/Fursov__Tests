import datetime

from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.utils.functions import form_days, date_to_point_format


class DynamicOrdersReport:
    """
    Динамика заказов поартикульно
    """

    def __init__(self, suppliers=None, date_from=None, date_to=None):
        self.__suppliers = suppliers

        if date_from is None and date_to is None:
            date_to = datetime.date.today()
            date_from = date_to - datetime.timedelta(7)
            self.days = form_days(7, dot_format=1, flag_today=0)

        self.__date_from = date_to_point_format(date_from.strftime("%Y-%m-%d"))
        self.__date_to = date_to_point_format(date_to.strftime("%Y-%m-%d"))

        self.__response = {}
        self.__drf_orders = {}

    def execute(self):
        print('====== Динамика заказов поартикульно ======')
        for supplier in self.__suppliers:
            print(f"\rОбрабатываем - {supplier.get('name')}")
            self.__get_nomenclatures(supplier.get('supplier-id'), supplier.get('name'), supplier.get('wb_token'))
            self.__get_data(supplier.get('supplier-id'), supplier.get('wb_token'), supplier.get('name'))
        return self.__get_table()

    def __get_nomenclatures(self, supplier_id, supplier_name, wb_token):
        """
        Получение номенклатур
        :param supplier_id: id поставщика
        :param supplier_name: имя поставщика
        :return:
        """
        data = PersonalAccountAPI.get_nomenclatures(supplier_id, wb_token)
        for nomenclature in data:

            if not self.__response.get(nomenclature['sa'] + supplier_name):
                self.__response[nomenclature['sa'] + supplier_name] = {'supplier': supplier_name,
                                                                       'article': nomenclature['sa'],
                                                                       'nm_id': nomenclature['nmID'],
                                                                       'brand': nomenclature['brandName'],
                                                                       'subject': nomenclature['subjectName'],
                                                                       'days': {}}

    def __get_data(self, supplier_id, wb_token, supplier_name):
        """
        Получение данных
        :param supplier_id: id поставщика
        :param supplier_name: имя поставщика
        :return:
        """

        response = PersonalAccountAPI.get_dynamic(supplier_id, wb_token, self.__date_from, self.__date_to)
        data = response[0]['data']['weeklyTables']

        self.__collect_top_brands(data)

        for brand in data:
            brand_name = brand['brand']
            for week in brand['weeks']:
                for day in week['days']:
                    date = day['day']
                    for orders in day['articles']:
                        article = orders['article']
                        pieces = orders['orderGoodsPiece']
                        price = round(orders['costPrice'] / 85 * 100)

                        if self.__response.get(article + supplier_name):
                            if self.__response.get(article + supplier_name)['days'].get(date):
                                self.__response[article + supplier_name]['days'][date][0] += price
                                self.__response[article + supplier_name]['days'][date][1] += pieces
                            else:
                                self.__response[article + supplier_name]['days'][date] = [price, pieces]
                        else:
                            self.__response[article + supplier_name] = {'supplier': supplier_name,
                                                                        'brand': brand_name,
                                                                        'nm_id': '-',
                                                                        'subject': '-', 'article': article,
                                                                        'days': {date: [price, pieces]}}

    def __get_table(self) -> list:
        """
        Формирование таблицы
        :return: list
        """
        table_head = ["Поставщик", "Бренд", "Предмет", "Номенклатура", "Артикул/Цвет", *self.days, 'Итого']
        table = [
            [table_head, ],
            [table_head, ],
        ]
        top_dict = []
        overall_count = 0
        overall_rub = 0
        zero_orders = 0

        for article in self.__response.values():
            days_sum_count = 0
            days_sum_rub = 0

            row_count = [
                article['supplier'],
                article['brand'],
                article['subject'],
                article['nm_id'],
                article['article']
            ]

            row_rub = [
                article['supplier'],
                article['brand'],
                article['subject'],
                article['nm_id'],
                article['article']
            ]

            iter_days = self.days
            for day in iter_days:
                orders_list = article['days'].get(day)
                if orders_list:

                    price = orders_list[0]
                    piece = orders_list[1]

                    row_count.append(piece)
                    row_rub.append(price)

                    if day != iter_days[-1]:
                        days_sum_count += piece
                        days_sum_rub += price

                else:
                    row_count.append(0)
                    row_rub.append(0)

            if not days_sum_rub:
                zero_orders += 1

            row_count.append(days_sum_count)
            row_rub.append(days_sum_rub)

            overall_rub += days_sum_rub
            overall_count += days_sum_count

            table[0].append(row_rub)
            table[1].append(row_count)

            top_dict.append((len(table[0]) - 1, days_sum_count))

        self.__collect_top_orders(table, top_dict)

        self.__drf_orders["baseStat"] = {
            "ordersCount": overall_count,
            "ordersRub": overall_rub,
            "ordersRows": len(table[0]) - 1,
            "ordersZero": zero_orders,
        }

        return table

    def __collect_top_orders(self, table: list, top_dict: list):

        self.__drf_orders["topOrders"] = []
        self.__drf_orders["topOrdersWeek"] = []

        top_dict.sort(key=lambda tup: tup[1], reverse=True)

        if len(top_dict) < 10:
            top_count = len(top_dict)
        else:
            top_count = 10

        for idx in range(top_count):
            row_rub = table[0][top_dict[idx][0]]
            row_count = table[1][top_dict[idx][0]]

            self.__drf_orders["topOrders"].append({
                "name": row_count[4],
                "nmId": row_count[3],
                "ordersAmount": row_count[-1],
                "ordersRub": row_rub[-1],
            })

            if idx < 5:
                self.__drf_orders["topOrdersWeek"].append({
                    "name": row_count[4],
                    "ordersAmount": row_count[5:12],
                })

    def __collect_top_brands(self, brands):
        self.__drf_orders["topBrands"] = []
        top_brands = []

        for brand in brands:
            top_brands.append((brand["brand"], brand["orderGoodsPiece"]))

        top_brands.sort(key=lambda tup: tup[1], reverse=True)

        if len(top_brands) < 5:
            top_count = len(top_brands)
        else:
            top_count = 5

        for idx in range(top_count):
            self.__drf_orders["topBrands"].append({
                "brand": top_brands[idx][0],
                "ordersAmount": top_brands[idx][1],
            })

    def get_drf_orders(self):
        return self.__drf_orders
