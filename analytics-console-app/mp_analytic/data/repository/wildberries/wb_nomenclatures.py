from config.constants import WB_TOKEN
from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from domain.utils.functions import get_suppliers_list


class NomenclaturesReport:
    def __init__(self, wb_token, suppliers=None):
        self.__wb_token = wb_token
        self.__suppliers = get_suppliers_list() if suppliers is None else get_suppliers_list(suppliers)
        self.__table = [['Поставщик', 'Бренд', 'Предмет', 'Номенклатура', 'Артикул/цвет', 'Размер']]

    def execute(self):
        print("====== ПЕРЕЧЕНЬ НОМЕНКЛАТУР ======")
        for supplier in self.__suppliers:
            print(f"Сбор данных по поставщику - {supplier['name']}")
            self.__get_nomenclatures(self.__wb_token, supplier['supplier-id'], supplier['name'])
        return self.__table

    def __get_nomenclatures(self, wb_token, supplier_id, supplier_name):
        data = PersonalAccountAPI.get_nomenclatures(supplier_id)

        for nomenclature in data:
            brand = nomenclature.get('brandName')
            subject = nomenclature.get('subjectName')
            nm = nomenclature.get('nmID')
            article = nomenclature.get('sa')
            size = nomenclature.get('tsName')
            self.__table.append([supplier_name, brand, subject, nm, article, size])


if __name__ == '__main__':
    print(NomenclaturesReport(WB_TOKEN).execute())
