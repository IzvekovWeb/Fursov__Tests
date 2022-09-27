import copy

from config.suppliers import SUPPLIERS
from data.marketplaces.wildberries.mpstats import MpStatsAPI
from data.marketplaces.wildberries.wb_orders_statistics import OrdersStatisticsWB
from data.utils.functions import form_days


class OrdersAllCategories(object):
    def __init__(self, category_list, day_count: int):
        self.__category_dict_mpst = {}
        self.table = []
        self.__days = form_days(day_count)
        self.__category_dict = {}
        self.__get_columns = category_list

    def execute_mpstats(self):
        get_columns = self.__get_columns
        for category in get_columns:
            response = MpStatsAPI().get_category_by_date(get_columns)
            self.get_data_mpstats(response, category)
        return self.create_table_mpstats()

    def get_data_mpstats(self, response, category):
        try:
            for elem in response:
                if not self.__category_dict_mpst.get(category.split('/')[-1]):
                    self.__category_dict_mpst[category.split('/')[-1]] = {elem['period']: {'count': elem['revenue']}}
                else:
                    if not self.__category_dict_mpst[category.split('/')[-1]].get(elem['period']):
                        self.__category_dict_mpst[category.split('/')[-1]][elem['period']] = {'count': elem['revenue']}
                    else:
                        self.__category_dict_mpst[category.split('/')[-1]][elem['period']]['count'] += elem['revenue']
        except Exception as e:
            print(f'Ошибка {e}')

    def create_table_mpstats(self) -> list:
        """
        :return: Table of tuples with resulted data
        """

        for category, day in self.__category_dict_mpst.items():  # Проходимся по категориям и дням
            summary = 0
            row = []  # Список со строкой для таблицы
            for day_column in self.__days:
                if not self.__category_dict_mpst[category].get(day_column):
                    row.append(0)
                    summary += 0
                else:
                    row.append(day[day_column]['count'])  # Вставляем сумму
                    summary += day[day_column]['count']
            else:
                self.table.append((category, *row, summary))
        return self.execute_wb()

    def execute_wb(self):
        for day in self.__days:  # Цикл по каждому дню из списка
            print(f"  | Сбор данных за {day}")
            for supplier in SUPPLIERS.values():  # Цикл по словарю поставщиков
                token = supplier.get('token')
                x64key = supplier.get('x64key')
                name = supplier.get('name')
                response = OrdersStatisticsWB().get_orders(token, x64key, day, name)
                self.get_data_wb(response, day)
        return self.create_table_wb()

    def get_data_wb(self, response, day):
        """
        :param response: Ответ с WB
        :param day: Выбранный день
        """
        for elem in response:

            # Вычисление стоимости с учетом скидки
            final_price = round(elem['totalPrice'] - elem['totalPrice'] * (elem['discountPercent'] / 100))

            if not self.__category_dict.get(elem['subject']):
                self.__category_dict[elem['subject']] = {day: {'count': final_price}}
            else:
                if not self.__category_dict[elem['subject']].get(day):
                    self.__category_dict[elem['subject']][day] = {'count': final_price}
                else:
                    self.__category_dict[elem['subject']][day]['count'] += final_price

    def create_table_wb(self) -> list:
        """
        :return: Table of tuples with resulted data
        """

        table = []
        for category, day in self.__category_dict.items():  # Проходимся по категориям и дням
            summary = 0
            row = []  # Список со строкой для таблицы
            for day_column in self.__days:
                if not self.__category_dict[category].get(day_column):
                    row.append(0)
                    summary += 0
                else:
                    row.append(day[day_column]['count'])  # Вставляем сумму
                    summary += day[day_column]['count']
            else:
                table.append((category, *row, summary))
        table.extend(self.table)
        return self.change_table(table)

    def change_table(self, table):
        count = []
        for value in table:
            table_copy = copy.deepcopy(table)
            index = table.index(value)
            table_copy.pop(index)
            for value_copy in table_copy:
                if value[0][0:5] == value_copy[0][0:5] and len(value[0]) == len(value_copy[0]):
                    count.append(value)
                    continue
        count = list(set(count))
        count.sort(key=lambda s: (s[0][0:5], len(s[0]), s[1]))
        return self.insert_percent_row(count)

    def insert_percent_row(self, count):
        table_category = [('Категория', *self.__days, 'Итог 7 дней')]
        table_copy = copy.deepcopy(count)
        for row in count:
            our_dynamic_row = []
            for elem in range(1, len(row) - 2):
                if elem + 1 != len(row) - 2:
                    our_day_dynamic = f'{round((int(row[elem + 1]) / int(row[elem]) - 1) * 100, 2)}%' if int(
                        row[elem]) != 0 else '0%'
                    our_dynamic_row.append(our_day_dynamic)
                else:
                    our_day_dynamic_1 = f'{round((int(row[elem + 1]) / int(row[elem]) - 1) * 100, 2)}%' if int(
                        row[elem]) != 0 else '0%'
                    our_dynamic_row.append(our_day_dynamic_1)
                    our_day_dynamic = f'{round((int(row[elem + 1]) / int(row[1]) - 1) * 100, 2)}%' if int(
                        row[1]) != 0 else '0%'
                    our_dynamic_row.append(our_day_dynamic)
                    break
            if count.index(row) % 2 == 0:
                table_copy.insert((count.index(row) + 1) * 2, ('Динамика наша', '', *our_dynamic_row))
                continue
            else:
                table_copy.insert(count.index(row) * 2 + 1, ('Динамика тренда', '', *our_dynamic_row))
                continue
        table_category.extend(table_copy)
        return table_category
