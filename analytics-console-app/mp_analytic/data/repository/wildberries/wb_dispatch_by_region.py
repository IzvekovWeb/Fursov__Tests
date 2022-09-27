from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from domain.utils.functions import get_suppliers_list
from datetime import date


class DispatchBYRegion(object):
    """
    Отчет "Отгрузка по регионгам"
    """

    def __init__(self, suppliers=None):
        self.dateFrom = date.today().strftime("%d.%m.%y")
        self.__suppliers = get_suppliers_list() if suppliers is None else get_suppliers_list(suppliers)  # suppliers
        self.__dis_by_reg = list()

    def execute(self) -> list:
        for supplier in self.__suppliers:
            self.get_orders(supplier.get('supplier-id'), supplier.get('WB_TOKEN'), supplier.get('name'))
        return self.__get_table()

    def get_orders(self, supplier_id, wb_token, supplier_name):
        id = PersonalAccountAPI.get_sales_id(supplier_id, self.dateFrom, self.dateFrom)
        data_dispatch = PersonalAccountAPI.get_sales(supplier_id, id)
        for rows in data_dispatch:
            for row in rows:
                self.__dis_by_reg.append(
                    {"Поставщик": supplier_name, "Артикул/цвет": f'{row.get("5")}/{row.get("8")}',
                     "Регион": row.get("10"),
                     "Заказано": row.get("12"),
                     "Остаток": row.get("16")})

    def __get_table(self):
        table = [("Поставщик", "Артикул/цвет", "Регион", "Заказано, шт.", "Остаток склад ВБ", "Отгрузка"), ]
        for item in self.__dis_by_reg:
            current_balance = item.get('Заказано')
            orders_amount = item.get('Остаток')
            supplier = item.get('Поставщик')
            stock = item.get('Регион')
            article = item.get("Артикул/цвет")
            if orders_amount.isdigit() and current_balance.isdigit():
                orders_amount, current_balance = int(orders_amount), int(current_balance)
                if current_balance < 5 and orders_amount < 5:
                    dispatch_amount = 20
                elif orders_amount < current_balance:
                    dispatch_amount = 0
                else:
                    dispatch_amount = orders_amount - current_balance
                table.append((supplier, stock, article, orders_amount, current_balance, dispatch_amount))
        return table

