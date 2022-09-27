from data.marketplaces.wildberries.wb_supplier_stat import SupplierStatAPI
from data.utils.functions import form_days, normalize_hour, normalize_price
from datetime import datetime

from domain.utils.functions import get_suppliers_list


class DynamicAllCategories:
    """
    Динамика по всем категориям
    """

    def __init__(self, wb_token, day_count: int, required_categories: list, suppliers=None):
        self.__wb_token = wb_token
        self.__suppliers = get_suppliers_list() if suppliers is None else get_suppliers_list(suppliers)
        self.__days = form_days(day_count, flag_today=0)  # List of dates
        self.__category_dict = {}  # Resulted dictionary
        self.__required_categories = required_categories  # Category's list from Google Sheet

    def execute(self):
        for day in self.__days:
            print(f"  | Сбор данных за {day}")
            for supplier in self.__suppliers:

                response = SupplierStatAPI.get_orders(supplier.get('token'), supplier.get('x64key'), day)
                self.__get_data(response, day)
        return self.__get_table(), len(self.__category_dict.keys()) + 1

    def __get_data(self, response, day):
        """
        :param response: Response from WB API
        :param day: Day
        """

        summary_price = 0  # Sum of all orders
        hour = 0  # Hour's counter [0 - 23]

        for elem in response:
            date = datetime.strptime(elem['date'], '%Y-%m-%dT%H:%M:%S')
            date_time_00 = datetime.strptime(f'{day}T{hour}:00:00', '%Y-%m-%dT%H:%M:%S')

            # Вычисление стоимости с учетом скидки
            final_price = round(elem['totalPrice'] - elem['totalPrice'] * (elem['discountPercent'] / 100), 2)
            if date > date_time_00:
                hour = date.hour

            category = elem['subject']
            if category not in self.__required_categories:
                category = 'Остальное'

            if not self.__category_dict.get(category):
                self.__category_dict[category] = {day: {f'count_{hour}': final_price}}

            else:
                if not self.__category_dict[category].get(day):
                    self.__category_dict[category][day] = {f'count_{hour}': final_price}

                elif not self.__category_dict[category][day].get(f'count_{hour}'):
                    tmp_dict = self.__category_dict[category][day]
                    last_value = 0

                    for tmp_hour in range(hour, -1, -1):
                        if tmp_dict.get(f'count_{tmp_hour}'):
                            last_value = tmp_dict[f'count_{tmp_hour}']
                            break

                    self.__category_dict[category][day][f'count_{hour}'] = \
                        last_value + final_price

                    for tmp_hour in range(hour + 1, 24):
                        if tmp_dict.get(f'count_{tmp_hour}'):
                            tmp_dict[f'count_{tmp_hour}'] += final_price

                else:
                    self.__category_dict[category][day][f'count_{hour}'] += final_price
                    tmp_dict = self.__category_dict[category][day]
                    for tmp_hour in range(hour + 1, 24):
                        if tmp_dict.get(f'count_{tmp_hour}'):
                            tmp_dict[f'count_{tmp_hour}'] += final_price

            summary_price += final_price

    def __get_table(self) -> list:
        """
        :return: Table of tuples with resulted data
        """

        table = [('Час', 'Категория', *self.__days), ]
        others = None

        for hour in range(0, 24):  # in range of hours
            normalized_hour = normalize_hour(hour)
            hour_summary = [0] * len(self.__days)
            for category, day in self.__category_dict.items():

                row = []
                for idx, day_column in enumerate(self.__days):
                    tmp_category_dict = self.__category_dict[category]
                    if not tmp_category_dict.get(day_column):
                        row.append(0)
                    else:
                        hour_line = day[day_column]
                        if not hour_line.get(f'count_{hour}'):
                            last_value = 0
                            for tmp_hour in range(hour, -1, -1):
                                if hour_line.get(f'count_{tmp_hour}'):
                                    last_value = hour_line[f'count_{tmp_hour}']
                                    last_value = normalize_price(last_value)
                                    break
                            row.append(last_value)
                            hour_summary[idx] += last_value
                            continue
                        tmp_price = normalize_price(hour_line[f'count_{hour}'])
                        row.append(tmp_price)  # Вставляем сумму
                        hour_summary[idx] += tmp_price
                if category != f'Итого' and category != 'Остальное':
                    table.append((normalized_hour, category, *row))
                elif category == 'Остальное':
                    others = list()
                    others.extend(row)
            if isinstance(others, list):
                table.append((normalized_hour, 'Остальное', *others))
            table.append((normalized_hour, f'Итого', *hour_summary))
        return table
