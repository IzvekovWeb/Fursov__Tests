from mp_analytic.data.utils.functions import form_days
from mp_analytic.config.suppliers import SUPPLIERS
from mp_analytic.data.marketplaces.wildberries.wb_orders_statistics import OrdersStatisticsWB


class OrdersAllCategories(object):
    def __init__(self, day_count: int):
        self.__days = form_days(day_count)
        self.__category_dict = {}
        self.__table_head = ['Категория']

    def execute(self):
        for day in self.__days:  # Цикл по каждому дню из списка
            print(f"  | Сбор данных за {day}")
            for supplier in SUPPLIERS.values():  # Цикл по словарю поставщиков
                token = supplier.get('token')
                x64key = supplier.get('x64key')
                name = supplier.get('name')
                url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/orders'

                response = OrdersStatisticsWB().get_orders(token, x64key, day, name)
                self.get_data(response, day)
        return self.create_table()

    def get_data(self, response, day):
        """
        :param response: Ответ с WB
        :param day: Выбранный день
        """

        summary_price = 0  # Итоговая сумма
        for elem in response:

            # Вычисление стоимости с учетом скидки
            final_price = round(elem['totalPrice'] - elem['totalPrice'] * (elem['discountPercent'] / 100), 2)

            if not self.__category_dict.get(elem['subject']):
                self.__category_dict[elem['subject']] = {day: {'count': final_price}}
            else:
                if not self.__category_dict[elem['subject']].get(day):
                    self.__category_dict[elem['subject']][day] = {'count': final_price}
                else:
                    self.__category_dict[elem['subject']][day]['count'] += final_price

            summary_price += final_price

        # Вставляем в словарь итоговую сумму
        try:
            self.__category_dict["Итого"][day]['count'] += summary_price
        except KeyError:
            if not self.__category_dict.get('Итого'):
                self.__category_dict["Итого"] = {day: {'count': summary_price}}
            else:
                self.__category_dict["Итого"][day] = {'count': summary_price}

    def normalize_price(self, price):
        return round((price / 85) * 100, 1)

    def create_table(self) -> list:
        """
        :return: Table of tuples with resulted data
        """

        table = [('Категория', *self.__days), ]
        summary = []
        for category, day in self.__category_dict.items():  # Проходимся по категориям и дням
            row = []  # Список со строкой для таблицы
            for day_column in self.__days:
                if not self.__category_dict[category].get(day_column):
                    row.append(0)
                else:
                    row.append(self.normalize_price(day[day_column]['count']))  # Вставляем сумму
            if category == 'Итого':
                summary.extend(row)
            else:
                table.append((category, *row))
        table.append(("Итого", *summary))  # В конце вставляем итог
        return table
