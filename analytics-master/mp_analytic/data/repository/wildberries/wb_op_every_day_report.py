from data.marketplaces.wildberries.wb_supplier_stat import SupplierStatAPI
from data.utils.functions import percent


class OPeveryDayReport(object):
    def __init__(self, days, suppliers=None):
        self.__suppliers = suppliers
        self.__days = days
        self.__response = {}
        self.__second_response = {}

    def execute(self):
        for day in self.__days:
            print(f"  | Сбор данных за {day}")
            for supplier in self.__suppliers:  # Цикл по словарю поставщиков
                token = supplier.get('token')
                x64key = supplier.get('x64key')

                orders_response = SupplierStatAPI.get_orders(token, x64key, day)
                if not self.__response.get(day):
                    self.__response[day] = {}

                self.__count_orders(orders_response, day)

        return self.__response

    def __count_orders(self, data: list, date):
        """
        :param data: Список полученных данных
        :param date: Дата
        """

        for row in data:
            category = f"{row['category'] + '/' + row['subject']}"  # Get category
            article = row['supplierArticle']
            if category in self.__response[date].keys():  # Check exists in dict
                self.__response[date][category]['total'] += percent(row['totalPrice'],
                                                                    row['discountPercent'])
                self.__response[date][category]['count'] += 1

                if article not in self.__response[date][category]['article'].keys():
                    self.__response[date][category]['article'][article] = 1
                else:
                    self.__response[date][category]['article'][article] += 1
            else:
                self.__response[date][category] = {
                    'article': {article: 1},
                    'category': category,
                    'count': 1,
                    'prime_cost': 0,
                    'percentage': 0.0,
                    'total': percent(row['totalPrice'], row['discountPercent'])
                }

    def normalize_price(self, price):
        return round((price / 85) * 100, 1)

    def create_table(self, response) -> list:
        table = [("Дата", "Категория", "Заказы, шт.", "Заказы, руб.",
                  "% выкупа", "Логистика", "Себестоимость",
                  "Продажи", "ОП"), ]

        for day in self.__days:
            total_cost_per_day = 0
            sold_profit_per_day = 0
            total_profit_per_day = 0

            for category, values in response[day].items():
                percentage = values['percentage'] / 100
                total_cost = values['total']
                try:
                    logistics = values['transition']
                except KeyError:
                    logistics = 0
                sell_count = values['count']
                prime_cost = values['prime_cost']

                prime_cost = prime_cost * percentage
                total_cost_to_insert = self.normalize_price(total_cost)
                sold_profit_to_insert = percentage * total_cost_to_insert
                sold_profit_to_insert = round(sold_profit_to_insert, 1)

                total_cost_per_day += total_cost_to_insert
                sold_profit_per_day += sold_profit_to_insert

                logistics_expenses = logistics * sell_count + 33 * sell_count * (1 - percentage)

                total_profit = (sold_profit_to_insert * 0.85 - logistics_expenses - prime_cost)
                total_profit = round(total_profit, 1)
                total_profit_per_day += total_profit

                table.append((day, category, sell_count,
                              total_cost_to_insert, f'{values["percentage"]}%',
                              logistics,
                              prime_cost,
                              sold_profit_to_insert,
                              total_profit))
            try:
                rent = round(total_profit_per_day / sold_profit_per_day * 100, 2)
            except ZeroDivisionError:
                rent = 0
            self.__second_response[day] = {
                "profit": round(total_profit_per_day, 1),
                "cost": round(total_cost_per_day, 1),
                "sold": round(sold_profit_per_day, 1),
                "rent": f"{rent}%"
            }

        return table

    def create_op_table(self):
        table = [('Дата', *self.__days)]
        keys = ("profit", "cost", "sold", "rent")
        keys_ru = ("ОП", "Заказы, руб.", "Продажи, руб.", "Рент")
        for idx, key in enumerate(keys):
            row = [keys_ru[idx]]
            for date in self.__second_response.keys():
                row.append(self.__second_response[date][key])
            table.append(row)
        return table
