from data.marketplaces.wildberries.mpstats import MpStatsAPI
from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.utils.functions import form_days
from domain.utils.functions import get_suppliers_list


class DynamicByNomenclatureCategory(object):
    """
    Отчет "Категории"
    """

    def __init__(self, wb_token: str, nomenclature_list: list, suppliers=None, day_count: int = 7):
        self.__wb_token = wb_token
        self.__suppliers = get_suppliers_list() if suppliers is None else get_suppliers_list(suppliers)
        self.__days = form_days(day_count, date_format="%d.%m")
        self.__nomenclature_list = nomenclature_list
        self.__response = {}

    def execute(self):
        print("====== ОТЧЕТ \"КАТЕГОРИИ\" ======")
        print("Сбор информации по номенклатурам...")
        for supplier in self.__suppliers:
            self.__get_nomenclatures(supplier['supplier-id'], supplier['name'])

        nomenclatures_positions = MpStatsAPI.get_sku_position(self.__nomenclature_list)
        return self.__get_table(nomenclatures_positions)

    def __get_nomenclatures(self, supplier_id, supplier_name):
        """
        Получение номенклатур
        :param supplier_id: id поставщика
        :param supplier_name: имя поставщика
        :return:
        """
        data = PersonalAccountAPI.get_nomenclatures(supplier_id)
        for nm in data:
            if nm['nmID'] in self.__nomenclature_list:
                self.__response[nm['nmID']] = {'supplier': supplier_name, 'article': nm['sa'], 'nm_id': nm['nmID'],
                                               'brand': nm['brandName'], 'subject': nm['subjectName']}

    def __get_table(self, nomenclatures_positions) -> list:
        """
        Формирование таблицы для выгрузки
        :param nomenclatures_positions: номенклатурные позиции
        :return: list of tuple
        """
        table = [('Организация', 'Номенклатура', 'Артикул поставщика', 'Предмет', 'Бренд', *self.__days)]
        for nomenclature in self.__nomenclature_list:
            if not self.__response.get(nomenclature):
                continue

            row = [self.__response[nomenclature]['supplier'], self.__response[nomenclature]['nm_id'],
                   self.__response[nomenclature]['article'], self.__response[nomenclature]['subject'],
                   self.__response[nomenclature]['brand']]

            for nomenclature_ in nomenclatures_positions:

                if not isinstance(nomenclature_, dict) or nomenclature not in nomenclature_.keys():
                    continue

                positions = nomenclature_[nomenclature]['categories']

                days = [0 for _ in range(7)]
                for category in positions:
                    for i in range(7):
                        if positions[category][i] != 'NaN':
                            days[i] += 1

                row.extend(days)
                table.append(tuple(row))
        return table
