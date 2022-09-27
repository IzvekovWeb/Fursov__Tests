import datetime
import multiprocessing

import pandas as pd

from config.suppliers import SUPPLIERS
from data.marketplaces.wildberries.wb_orders_statistics import OrdersStatisticsWB
from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.utils.functions import form_days


class OrdersPosition(object):
    def __init__(self, category_list: list = [], nomenclature_list: list = [], day_count: int = 7):
        self.table_head = ['Организация', "Номенклатура", "Артикул поставщика", "Предмет", 'Бренд', 'Категория']
        self.days = form_days(day_count)
        self.category_list = category_list
        self.nomenclature_list = nomenclature_list

    def execute(self):
        wb_data = self.get_wb_data()
        dataframe_wb = self.create_df_and_add_report_wb(wb_data)

        mpstats_list_with_count = self.get_mpstats_data(self.category_list)

        df = self.add_mpstats_list_from_df(dataframe_wb, mpstats_list_with_count)
        formatted_data = self.formatting_df(df)
        return self.create_table(formatted_data)

    def create_table(self, response):
        table = [(*self.table_head, *self.days), ]
        table.extend(response)
        return table

    def get_wb_data(self):
        wb_data = []
        wb_data_dict = {}

        for supplier in SUPPLIERS.values():
            supplier_id = supplier.get("supplier-id")
            supplier_name = supplier.get("name")

            print(f"\rОбрабатываем - {supplier_name}")

            data = PersonalAccountAPI.get_nomenclatures(supplier_id)

            for nomenclature in data:
                main_key = nomenclature["sa"] + supplier_name
                if not wb_data_dict.get(main_key):
                    wb_data_dict[main_key] = {'supplier': supplier_name,
                                              'article_color': nomenclature["sa"],
                                              'nm_id': nomenclature['nmID'],
                                              'brand': nomenclature['brandName'],
                                              'subject': nomenclature['subjectName']}

        for row in wb_data_dict.values():
            if row["nm_id"] in self.nomenclature_list:
                wb_data.append([
                    row["supplier"],
                    row["nm_id"],
                    row["article_color"],
                    row["subject"],
                    row["brand"]
                ])
        return wb_data

    def create_df_and_add_report_wb(self, response_data):
        df = self.build_wb_df()
        for j in response_data:
            df2 = self.build_wb_df(j)
            df = pd.concat([df, df2])

        return df

    def build_wb_df(self, data=None):
        if not data:
            df = pd.DataFrame({"Организация": [],
                               "Номенклатура": [],
                               "Артикул Поставщика": [],
                               "Предмет": [],
                               "Бренд": [],
                               })
        else:
            df = pd.DataFrame({"Организация": [data[0]],
                               "Номенклатура": [data[1]],
                               "Артикул Поставщика": [data[2]],
                               "Предмет": [data[3]],
                               "Бренд": [data[4]],
                               })

        return df

    def formiratting_lists_in_list(self, list_wb):
        a = len(list_wb) // 42
        nm_lists_in_list = []
        for i in range((len(list_wb) // 42) + 1):
            if i == a + 1:
                nm_lists_in_list.append(list_wb[0 + (42 * i):])
            nm_lists_in_list.append(list_wb[0 + (42 * i):42 + (42 * i)])

        return nm_lists_in_list

    def get_mpstats_data(self, real_categories):
        nm_lists_in_list = self.formiratting_lists_in_list(self.nomenclature_list)

        mul_list = []
        foo = OrdersStatisticsWB().get_mpstats_response
        with multiprocessing.Pool(5) as pool:
            mul_list += pool.map(foo, nm_lists_in_list)

        nm_data = []
        for i in range(len(mul_list)):
            nm_data.extend(mul_list[i])

        nm_with_out_card = []
        for i in nm_data:
            if type(i) == int:
                nm_with_out_card.append(i)

        for i in nm_with_out_card:
            nm_data.remove(i)

        mpstats_list_with_count = []
        count_other = 0
        for z in nm_data:
            sales = []
            if isinstance(z, dict):
                for k, v in z.items():
                    sales.append(k)

                    for categories in v['categories']:
                        split_categories = categories.split('/')
                        for real_categ in real_categories:
                            if split_categories[-1] == 'Костюм спортивный':
                                sales.append(categories)
                                sales.extend(v['categories'][categories])
                                break

                            elif categories == real_categ:
                                count_other += 1
                                sales.append(categories)
                                sales.extend(v['categories'][categories])
                                break

            if len(sales) == 1:
                sales.extend(['Нет значения', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'])
            mpstats_list_with_count.append(sales)

        for i in range(len(nm_with_out_card)):
            nm_with_out_card[i] = [nm_with_out_card[i], 'Нет значения', 'Нет значения', 'Нет значения', 'Нет значения',
                                   'Нет значения', 'Нет значения', 'Нет значения', 'Нет значения']

        data = mpstats_list_with_count + nm_with_out_card
        return data

    def add_mpstats_list_from_df(self, wb_df, mpstats_list_with_count):
        df = self.build_mpstats_df()
        for i in mpstats_list_with_count:
            df2 = self.build_mpstats_df(i)
            df = pd.concat([df, df2])

        df = self.merge_df(df, wb_df)

        return df

    def merge_df(self, df, wb_df):
        df = pd.merge(wb_df, df, on='Номенклатура')

        return df

    def formatting_df(self, df):
        num = 1
        date = []
        for _ in range(7):
            day = datetime.datetime.today() - datetime.timedelta(days=num)
            date.append(day.strftime("%d.%m.%Y"))
            num += 1

        for i in range(len(date)):
            df.loc[(df[date[i]] == 'NaN'), date[i]] = 0
            df.loc[(df[date[i]] == 'Нет значения'), date[i]] = 1
            df[date[i]] = df[date[i]].astype(int)
            df.loc[(df[date[i]] == 0), date[i]] = '-'
            df.loc[(df[date[i]] == 1), date[i]] = 'Нет значения'

        df['Номенклатура'] = df['Номенклатура'].astype(int)

        return df.values.tolist()

    def build_mpstats_df(self, data=None):
        num = 1
        all_date = []
        for _ in range(7):
            day = datetime.datetime.today() - datetime.timedelta(days=num)
            all_date.append(day.strftime("%d.%m.%Y"))
            num += 1

        if not data:
            df = pd.DataFrame({"Номенклатура": [],
                               'Категория': [],
                               all_date[0]: [],
                               all_date[1]: [],
                               all_date[2]: [],
                               all_date[3]: [],
                               all_date[4]: [],
                               all_date[5]: [],
                               all_date[6]: []
                               })

        else:
            df = pd.DataFrame({"Номенклатура": [data[0]],
                               'Категория': [data[1]],
                               all_date[0]: [data[2]],
                               all_date[1]: [data[3]],
                               all_date[2]: [data[4]],
                               all_date[3]: [data[5]],
                               all_date[4]: [data[6]],
                               all_date[5]: [data[7]],
                               all_date[6]: [data[8]]
                               })

        return df

    def getting_the_necessary_data(self, result_table, response_wb, supplier):
        # заберем из запроса карточки
        cards = response_wb.json()['result']['cards']

        for cards_item in cards:  # пробежим по каждой карточке из полученного списка
            brand = ''  # сначала название бренда пустое

            for addin in cards_item['addin']:
                if addin['type'] == "Бренд":
                    # если в addin карточки был параметр Бренд - запишем его
                    brand = addin['params'][0]['value']

            # бежим по номенклатурам из карточки
            for nomenclature in cards_item['nomenclatures']:
                if nomenclature['nmId'] not in self.nomenclature_list:
                    continue
                name = supplier.get('name')  # Название поставщика
                nm = nomenclature['nmId']  # Номенклатура
                article = cards_item.get('supplierVendorCode') + nomenclature['vendorCode']  # Артикул
                predmet = cards_item.get('object')  # Предмет

                result_table.append([
                    name,
                    nm,
                    article,
                    predmet,
                    brand
                ])
