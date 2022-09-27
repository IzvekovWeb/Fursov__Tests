import pandas as pd

from config.suppliers import SUPPLIERS
from data.marketplaces.wildberries.wb_orders_statistics import OrdersStatisticsWB
from data.utils.functions import form_days


class ReportMaxCategory(object):
    def __init__(self, category_list):
        self.__category_list = category_list
        self.__nomenclature_list = list()
        self.__head = list()

    def execute(self):
        response_list = self.mp_stats_category_post()
        self.get_headlines()
        dataa = self.mp_stats_by_category_get(response_list)
        df = self.finding_the_necessary_data(dataa)
        all_categ = self.get_mpstats_all_categories()
        necessary_data = self.get_necessary_data(df, all_categ)

        self.__nomenclature_list.clear()
        del response_list
        del dataa
        return self.create_table(necessary_data)

    def get_necessary_data(self, df, all_categ):
        for i in range(len(df)):
            df[i].append(list(all_categ[i][self.__nomenclature_list[i]]['categories'].keys()))

        return df

    def get_mpstats_all_categories(self):
        response_list = OrdersStatisticsWB().get_mpstats_response(self.__nomenclature_list)

        return response_list

    def mp_stats_category_post(self):
        foo = OrdersStatisticsWB().get_mpstats_response_max_categories
        response_list = []
        for category in self.__category_list:
            response_json = foo(category)
            for datas in response_json:
                for data in datas['data']:
                    response_list.append((
                        data['id'],
                        category,
                        data['category_graph']
                    ))
        return response_list

    @staticmethod
    def mp_stats_by_category_get(responses):
        response_json = []
        for i in responses:
            nomenclature = i[0]
            category = i[1]
            category_graph = i[2]
            response_json.append((
                nomenclature,
                category,
                *category_graph
            ))
        return response_json

    def finding_the_necessary_data(self, data):
        df = pd.DataFrame(data=data, columns=self.__head)
        df = df.groupby(by='Основная категория')[self.__head[2:]].max().reset_index()

        df = df.values.tolist()

        for j in df:
            for i in data:
                if i[1] == j[0] and i[-1] == j[-1]:
                    self.__nomenclature_list.append(i[0])
                    break

        return df

    def get_article_nomenclature(self):
        """
        :return: Response with card list
        """
        response_result = []
        for supplier in SUPPLIERS.values():
            response = OrdersStatisticsWB().get_cards(supplier)
            if not response:
                continue

            cards = response.json()['result']['cards']
            for cards_item in cards:

                for nomenclature in cards_item['nomenclatures']:
                    if nomenclature['nmId'] in self.__nomenclature_list:
                        article = cards_item['supplierVendorCode'] + nomenclature['vendorCode']
                        response_result.append((article, nomenclature['nmId']))
        return response_result

    def create_table(self, necessary_data):
        for value in necessary_data:
            self.__nomenclature_list.append(value[0])
        tab = self.get_article_nomenclature()
        for values in necessary_data:
            for art_nm in tab:
                if values[0] == art_nm[1]:
                    values.insert(1, art_nm[0])
                    break

            str_category = '\n'.join(values[-1])
            values[-1] = str_category
        self.__head.append('Все категории')
        self.__head.pop(0)
        necessary_data.insert(0, self.__head)
        return necessary_data

    def get_headlines(self):
        days = form_days(7)
        self.__head = ['Номенклатура', 'Основная категория', *days]
