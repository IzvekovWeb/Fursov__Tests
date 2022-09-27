import datetime

from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.marketplaces.wildberries.wb_supplier_stat import SupplierStatAPI
from data.utils.functions import form_days, date_to_point_format
from domain.utils.functions import get_suppliers_list


class Dispatch(object):
    """
    Отчет "Отгрузка"
    """

    def __init__(self, day_count: int, wb_token, suppliers=None):
        self.__wb_token = wb_token
        self.__suppliers = get_suppliers_list() if suppliers is None else get_suppliers_list(suppliers)  # suppliers
        self.__days = form_days(day_count)  # day list
        self.__stocks = dict()
        self.__new_nm_size = dict()
    def execute(self, table) -> list:
        print('========== ОТЧЕТ "ОТГРУЗКА" ==========')
        for supplier in self.__suppliers:
            print(f"Сбор отстатков для поставщика - {supplier.get('name')}")
            self.__get_stocks(supplier.get('name'), supplier.get('supplier-id'))
            self.__get_nomenclature(supplier.get('supplier-id'), table, supplier.get('name'))
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

    def __get_stocks(self, supplier_name: str, supplier_id: str):
        """
        Сбор остатков на складах
        :param supplier_name:
        :param supplier_id:
        :return:
        """
        date_from = date_to_point_format(datetime.date.today().strftime('%Y-%m-%d'))
        response = PersonalAccountAPI.get_stocks(supplier_id, date_from, date_from)

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

    def __get_nomenclature(self, supplier_id, table, supplier_name):
        nomenclature = PersonalAccountAPI.get_nomenclatures(supplier_id)
        for nm in nomenclature:
            sa_tsname = f"{nm.get('sa')}/{nm.get('tsName')}"
            for key, values in self.__stocks.items():
                if sa_tsname not in values:
                    for row in table:
                        if sa_tsname in row:
                            self.__new_nm_size[supplier_name] = dict()
                            self.__new_nm_size[supplier_name][sa_tsname] = row[8]

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

        for supplier, articles in self.__new_nm_size.items():
            for article, values in articles.items():
                orders_amount = 0
                current_balance = 0
                if int(values) < 20:
                    dispatch_amount = values
                else:
                    dispatch_amount = 20
                table.append((supplier, article, orders_amount, current_balance, dispatch_amount))
        return table
