import datetime

from data.marketplaces.ozon.api import OzonAPI
from data.utils.functions import form_days
from domain.utils.functions import get_suppliers_list_ozon


class OzonDynamicCount:
    def __init__(self, date_from=None, date_to=None, suppliers=None):
        self.__suppliers = get_suppliers_list_ozon(suppliers) if suppliers is not None else get_suppliers_list_ozon()
        if date_from is None and date_to is None:
            date_to = datetime.date.today()
            date_from = date_to - datetime.timedelta(7)

        self.__date_from = date_from.strftime("%Y-%m-%d")
        self.__date_to = date_to.strftime("%Y-%m-%d")
        self.__days = form_days(7)
        self.orders = []
        self.__response = {}
        self.__categories = set()
        self.__categories_dict = dict()

    def execute(self):
        for supplier in self.__suppliers:
            print(f"Обрабатываем поставщика - {supplier['name']}")
            self.__get_products(supplier['client_id'], supplier['api_key'], supplier['name'])
            self.__get_orders(supplier['client_id'], supplier['api_key'], supplier['name'])
            self.__get_categories(supplier['client_id'], supplier['api_key'])

        return self.__get_table()

    def __get_products(self, supplier_id, supplier_token, supplier_name):
        product_ids = [i['product_id'] for i in OzonAPI.get_product_list(supplier_id, supplier_token)]
        data = OzonAPI.get_products_info(supplier_id, supplier_token, product_ids)

        for i in data:
            article = i['offer_id']
            category = i['category_id']
            sku = '-'
            for j in i['sources']:
                if j['source'] == 'fbo':
                    sku = str(i['sources'][1]['sku'])

            self.__categories.add(category)

            self.__response[sku] = {'supplier': supplier_name, 'article': article, 'category': category, 'sku': sku,
                                    'days': {}}

    def __get_categories(self, supplier_id, supplier_token):
        while self.__categories:
            category_id = self.__categories.pop()
            title = OzonAPI.get_category_title(supplier_id, supplier_token, category_id)['result'][0]['title']
            self.__categories_dict[category_id] = title

    def __get_orders(self, supplier_id, supplier_token, supplier_name):
        data = OzonAPI.get_orders(supplier_id, supplier_token, datetime.date.today() - datetime.timedelta(7),
                                  datetime.date.today() - datetime.timedelta(1))
        for i in data:
            sku = i.get('dimensions')[1].get('id')
            day = i.get('dimensions')[0].get('id')
            count = i.get('metrics')[1]
            if self.__response.get(sku):
                if self.__response.get(sku)['days'].get(day):
                    self.__response[sku]['days'][day] += count
                else:
                    self.__response[sku]['days'][day] = count
            else:
                self.__response[sku] = {'supplier': supplier_name, 'category': '-', 'article': '-', 'sku': sku,
                                        'days': {day: count}}

    def __get_table(self):
        table = [['Организация', 'SKU', "Артикул", "Предмет", *self.__days, 'Итого']]
        for article in self.__response.values():
            days_sum = 0
            row = [article['supplier'], article['sku'], article['article'],
                   self.__categories_dict.get(article['category'])]
            for day in self.__days:
                pieces = article['days'].get(day)
                if pieces:
                    days_sum += pieces
                    row.append(pieces)
                else:
                    row.append(0)
            row.append(days_sum)
            table.append(row)
        return table


if __name__ == '__main__':
    print(OzonDynamicCount().execute())
