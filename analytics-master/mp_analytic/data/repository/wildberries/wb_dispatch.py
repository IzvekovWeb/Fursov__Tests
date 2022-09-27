import datetime

from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.marketplaces.wildberries.wb_supplier_stat import SupplierStatAPI
from data.utils.functions import form_days, date_to_point_format


class Dispatch(object):
    """
    Отчет "Отгрузка"
    """

    def __init__(self, day_count: int, suppliers=None):
        self.__suppliers = suppliers
        self.__days = form_days(day_count)  # day list
        self.__stocks = dict()

    def execute(self) -> list:
        print('========== ОТЧЕТ "ОТГРУЗКА" ==========')
        for supplier in self.__suppliers:
            print(f"Сбор отстатков для поставщика - {supplier.get('name')}")
            self.__get_stocks(supplier.get('name'), supplier.get('supplier-id'), supplier.get('wb_token'))

        for day in self.__days:
            print(f"  | Сбор данных за {day}")
            for supplier in self.__suppliers:
                self.__get_orders(supplier.get('token'), supplier.get('x64key'), day, supplier.get('name'))

        return self.__get_table()

    def __get_orders(self, token, key, day, supplier_name):
        data = SupplierStatAPI.get_orders(token, key, day)
        for row in data:  # Цикл по номенклатурам из списка
            article_size = row["supplierArticle"] + '/' + row['techSize']  # Артикул/Цвет/Размер

            if article_size not in self.__stocks[supplier_name].keys():
                self.__stocks[supplier_name][article_size] = {
                    'orders_amount': 1,
                    'currentBalance': 0,
                }
            else:
                try:
                    self.__stocks[supplier_name][article_size]['orders_amount'] += 1
                except KeyError:
                    continue

    def __get_stocks(self, supplier_name: str, supplier_id: str, wb_token: str):
        """
        Сбор остатков на складах
        :param supplier_name:
        :param supplier_id:
        :return:
        """
        date_from = date_to_point_format(datetime.date.today().strftime('%Y-%m-%d'))
        response = PersonalAccountAPI.get_stocks(supplier_id, wb_token, date_from, date_from)

        if not response:
            print(f"There are no data for {supplier_name}")
            return

        data = response[0]['data']['weeklyReportBalance']

        if supplier_name not in self.__stocks.keys():
            self.__stocks[supplier_name] = {}

        for row in data:
            for article in row['articles']:
                self.__stocks[supplier_name][f"{article['article']}/{article['size']}"] = {
                    'currentBalance': article['currentBalance'],
                    'orders_amount': 0
                }

    def __get_table(self):
        table = [("Поставщик", "Артикул", "Заказано, шт.", "Остаток склад ВБ", "Отгрузка"), ]

        for supplier, articles in self.__stocks.items():
            for article, values in articles.items():
                current_balance = values['currentBalance']
                orders_amount = values['orders_amount']

                dispatch_amount = orders_amount - current_balance

                if current_balance < 5 and orders_amount < 5:
                    dispatch_amount = 20

                if dispatch_amount < 0:
                    dispatch_amount = 0

                table.append((supplier, article, orders_amount, current_balance, dispatch_amount))

        return table
