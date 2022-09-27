from config.suppliers import SUPPLIERS
from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from config.get_ware_house import get_ware_house


class StocksByRegionReport:
    def __init__(self):
        self.__stocks = {}
        self.__suppliers = SUPPLIERS.values()
        self.__ware_house = get_ware_house()

    def execute(self):
        for supplier in self.__suppliers:
            supplier_id = supplier.get('supplier-id')
            supplier_name = supplier.get('name')
            stocks = PersonalAccountAPI().get_stocks_by_region(supplier_id)
            self.__stocks_iteration(stocks, supplier_name)

        return self.__create_table()

    def __stocks_iteration(self, stocks, supplier_name):
        for stock in stocks:
            try:
                stock_data = stock.get("data")
                balance_list = stock_data.get("balances")
                for balance in balance_list:
                    self.__collect_stocks(balance, supplier_name)
            except (KeyError, AttributeError) as err:
                print(err)
                continue

    def __collect_stocks(self, balance, supplier_name):
        article_color = balance["supplierArticle"]
        size = balance["techSize"]
        article_color_size = article_color + "/" + size

        if supplier_name not in self.__stocks.keys():
            self.__stocks[supplier_name] = {}

        self.__stocks[supplier_name][article_color_size] = balance
        self.__stocks[supplier_name][article_color_size].pop("supplierArticle")
        self.__stocks[supplier_name][article_color_size].pop("techSize")

    def __create_table(self):
        ware_house_titles = list(self.__ware_house.values())
        table = [("Поставщик", "Бренд", "Категория",
                  "Артикул/Цвет/Размер", "Номенклатура",
                  "Товары в пути", "Итого по складам",
                  *ware_house_titles)]

        for supplier_name, article_color_sizes in self.__stocks.items():
            for article_color_size, values in article_color_sizes.items():
                tmp_ware_house_quantity = []
                brand = values["brand"]
                category = values["subject"]
                nm_id = values["nmId"]
                quantity_in_transit = values['quantityInTransit']
                quantity_for_sale_total = values['quantityForSaleTotal']
                if not quantity_for_sale_total:
                    quantity_for_sale_total = 0

                for ware_house_key in self.__ware_house.keys():  # Collect warehouse's quantity
                    if ware_house_key in values.keys():
                        ware_house_quantity = values[ware_house_key]
                        if ware_house_quantity:
                            tmp_ware_house_quantity.append(ware_house_quantity)
                        else:
                            tmp_ware_house_quantity.append(0)

                row = (supplier_name, brand, category, article_color_size,
                       nm_id, quantity_in_transit, quantity_for_sale_total,
                       *tmp_ware_house_quantity)  # Create row to table
                table.append(row)

        return table


if __name__ == '__main__':
    StocksByRegionReport().execute()
