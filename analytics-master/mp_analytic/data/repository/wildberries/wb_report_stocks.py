import datetime

from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.utils.functions import date_to_point_format


class StocksReport:
    def __init__(self, date_from=None, date_to=None, suppliers=None):
        self.__suppliers = suppliers
        if date_from is None and date_to is None:
            date_from = datetime.date.today().strftime('%Y-%m-%d')
            date_to = date_from

        self.__response = {}
        self.__table = [["Поставщик", "Бренд", "Артикул/Цвет/Размер", "Артикул/Цвет", "Остатки в шт"]]
        self.__date_from = date_to_point_format(date_from)
        self.__date_to = date_to_point_format(date_to)

    def execute(self):
        for supplier in self.__suppliers:
            self.get_data(supplier)
        return self.__table

    def get_data(self, supplier: dict):
        response = PersonalAccountAPI.get_stocks(supplier.get('supplier-id'), supplier.get('wb_token'), self.__date_from, self.__date_to)
        if not response:
            print(f"There are no data for {supplier.get('name')}")
            return

        data = response[0]['data']['weeklyReportBalance']

        for i in data:
            brand = i['brand']
            for j in i['articles']:
                self.__table.append(
                    [supplier['name'], brand, f"{j['article']}/{j['size']}", j['article'], j['currentBalance']])
