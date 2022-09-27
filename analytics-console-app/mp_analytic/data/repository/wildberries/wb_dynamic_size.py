import datetime

from mp_analytic.config.suppliers import SUPPLIERS
from mp_analytic.data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from mp_analytic.data.utils.functions import form_days, date_to_point_format


class DynamicSizeReport:
    def __init__(self, date_from=None, date_to=None):
        if date_from is None and date_to is None:
            date_to = datetime.date.today() - datetime.timedelta(1)
            date_from = date_to - datetime.timedelta(6)

        self.date_from = date_to_point_format(date_from.strftime("%Y-%m-%d"))
        self.date_to = date_to_point_format(date_to.strftime("%Y-%m-%d"))
        self.days = form_days(7, dot_format=1)
        self.response = {}
        self.__table = [
            ["Поставщик", "Бренд", "Предмет", "Номенклатура", "Артикул/Цвет/Размер", *self.days, 'Итого']]

    def forming_nomenclatures(self, supplier_id, name):
        data = PersonalAccountAPI.get_nomenclatures(supplier_id)
        for nm in data:
            article = f"{nm['sa']}/{nm['tsName']}"
            if not self.response.get(article):
                self.response[article] = {'supplier': name, 'article': article, 'nm_id': nm['nmID'],
                                          'brand': nm['brandName'], 'subject': nm['subjectName'], 'days': {}}

    def execute(self):
        for supplier in SUPPLIERS.values():
            name = supplier.get('name')
            print(f"\rОбрабатываем - {name}{(' ' * (20 - len(name)))}")
            self.forming_nomenclatures(supplier['supplier-id'], name)
            self.get_data(supplier)
        return self.mapping_data()

    def get_data(self, supplier):
        response = PersonalAccountAPI.get_dynamic(supplier['supplier-id'], self.date_from, self.date_to)
        data = response[0]['data']['weeklyTables']

        for brand in data:
            brand_name = brand['brand']
            for week in brand['weeks']:
                for day in week['days']:
                    date = day['day']
                    for orders in day['articles']:
                        article = orders['article']
                        pieces = orders['orderGoodsPiece']

                        if self.response.get(article):
                            if self.response.get(article)['days'].get(date):
                                self.response[article]['days'][date] += pieces
                            else:
                                self.response[article]['days'][date] = pieces
                        else:
                            self.response[article] = {'supplier': supplier['name'], 'brand': brand_name, 'nm_id': '-',
                                                      'subject': '-', 'article': article, 'days': {date: pieces}}

    def mapping_data(self):
        for article in self.response.values():
            days_sum = 0
            row = [article['supplier'], article['brand'], article['subject'], article['nm_id'], article['article']]
            for day in self.days:
                pieces = article['days'].get(day)
                if pieces:
                    days_sum += pieces
                    row.append(pieces)
                else:
                    row.append(0)
            row.append(days_sum)
            self.__table.append(row)
        return self.__table

# class DynamicSizeReport:
#     def __init__(self, wb_token, suppliers=None):
#         self.__wb_token = wb_token
#         self.__suppliers = get_suppliers_list() if suppliers is None else get_suppliers_list(suppliers)
#
#         self.__days = form_days(7)
#         self.__response = {}
#
#     def execute(self):
#         print('====== ОТЧЕТ "ЗАКАЗЫ (ВСЕ)" ======')
#
#         for supplier in self.__suppliers:
#             print(f'Сбор номенклатур для поставщика - {supplier.get("name")}')
#             self.__get_nomenclatures(supplier.get('supplier-id'), supplier.get('name'))
#
#         for day in self.__days:
#             for supplier in self.__suppliers:
#                 print(f"\rОбрабатываем - {supplier.get('name')}")
#                 self.get_data(supplier.get('token'), supplier.get('x64key'), day, supplier.get('name'))
#         return self.__get_table()
#
#     def __get_nomenclatures(self, supplier_id, supplier_name):
#         data = PersonalAccountAPI.get_nomenclatures(supplier_id)
#         for nm in data:
#             article = f"{nm['sa']}/{nm['tsName']}"
#             if not self.__response.get(nm['nmID']):
#                 self.__response[nm['nmID']] = {'supplier': supplier_name, 'article': article, 'nm_id': nm['nmID'],
#                                                'brand': nm['brandName'], 'subject': nm['subjectName'], 'days': {}}
#
#     def get_data(self, token, key, day, supplier_name):
#         data = SupplierStatAPI.get_orders(token, key, day, supplier_name)
#
#         for row in data:  # Цикл по номенклатурам из списка
#             article_size = row["supplierArticle"] + '/' + row['techSize']  # Артикул/Цвет/Размер
#
#             if self.__response.get(row['nmid']):
#                 if self.__response.get(row['nmid'])['days'].get(day):
#                     self.__response[row['nmid']]['days'][day] += 1
#                 else:
#                     self.__response[row['nmid']]['days'][day] = 1
#             else:
#                 self.__response[row['nmid']] = {'supplier': supplier_name, 'brand': row['brand'], 'nm_id': row['nmid'],
#                                                 'subject': row['subject'], 'article': article_size, 'days': {day: 1}}
#
#     def __get_table(self):
#         table = [["Поставщик", "Бренд", "Предмет", "Номенклатура", "Артикул/Цвет/Размер", *self.__days, 'Итого']]
#         for article in self.__response.values():
#             days_sum = 0
#             row = [article['supplier'], article['brand'], article['subject'], article['nm_id'], article['article']]
#             for day in self.__days:
#                 pieces = article['days'].get(day)
#                 if pieces:
#                     days_sum += pieces
#                     row.append(pieces)
#                 else:
#                     row.append(0)
#             row.append(days_sum)
#             table.append(row)
#         return table
#
#
# if __name__ == '__main__':
#     DynamicSizeReport(WB_TOKEN).execute()
