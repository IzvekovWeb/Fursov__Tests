import datetime

from data.marketplaces.wildberries.wb_supplier_stat import SupplierStatAPI
from data.utils.functions import form_days


class OrdersTopReport(object):
    def __init__(self, day_count, nomenclature_list, suppliers=None):
        self.__suppliers = suppliers
        self.__days = form_days(day_count)  # Список дней
        self.__response = {}
        self.__nomenclature_list = nomenclature_list

    def execute(self) -> list:
        for day in self.__days:  # Цикл по каждому дню из списка
            print(f"  | Сбор данных за {day}")
            for supplier in self.__suppliers:  # Цикл по словарю поставщиков
                token = supplier.get('token')
                x64key = supplier.get('x64key')

                orders_response = SupplierStatAPI.get_orders(token, x64key, day)

                self.__count_orders(orders_response, day)

        return self.__mapping_dict_to_list()

    def modify_dict(self, categories_list: list):
        """
        :param categories_list: Список категорий
        """

        # Цикл по категориям для построения структуры словаря {"Категория": {"Дата": 0}}
        for each in categories_list:
            self.__response[each] = dict()
            for order_day in self.__days:
                self.__response[each][order_day] = {"count": 0}

    def __count_orders(self, data: list, date: datetime.date):
        """
        :param data: Список полученных данных
        :param date: Дата
        """

        summary_value = 0  # Суммарная стоимость заказов
        for elem in data:
            if elem['nmId'] in self.__nomenclature_list:
                final_price = round(elem['totalPrice'] - elem['totalPrice'] * (elem['discountPercent'] / 100), 2)
                summary_value += final_price
                if elem['subject'] in self.__response.keys():
                    self.__response[elem['subject']][date]['count'] += final_price
                else:
                    self.__response['Остальное'][date]['count'] += final_price

        self.__response['Итого'][date]['count'] += summary_value

    def __mapping_dict_to_list(self) -> list:
        """
        :return: Список из списков данных
        """

        table = [["Заказано руб.", *self.__days], ]  # Создаем список, первый элемент - кортеж заголовков

        for category, day in self.__response.items():
            row = [category]
            for val in day.values():
                row.append(val['count'])
            table.append(row)
        return table
