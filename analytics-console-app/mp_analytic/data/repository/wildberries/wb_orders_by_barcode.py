from data.utils.functions import form_days
from config.suppliers import SUPPLIERS
from data.marketplaces.wildberries.wb_orders_statistics import OrdersStatisticsWB


class OrdersByBarcode(object):
    def __init__(self, day_count: int):
        self.__days = form_days(day_count)
        self.__orders_dict = {}
        self.__table_head = ['Штрихкод', 'Номенклатура', 'Категория/Предмет', 'Артикул/Цвет/Размер', 'Размер']

    def execute(self):
        for day in self.__days:  # Цикл по каждому дню из списка
            print(f"  | Сбор данных за {day}")

            barcode_dict = {}
            for supplier in SUPPLIERS.values():  # Цикл по словарю поставщиков
                token = supplier.get('token')
                x64key = supplier.get('x64key')
                name = supplier.get('name')

                response = OrdersStatisticsWB().get_orders(token, x64key, day, name)
                self.get_data(response, day, barcode_dict)
        return self.create_table()

    def get_data(self, response, day, barcode_dict):
        for elem in response:
            if not barcode_dict.get(elem['barcode']) and len(elem['barcode']):
                barcode_dict[elem['barcode']] = {
                    "nmId": elem['nmId'],
                    "category": elem['category'] + "/" + elem['subject'],
                    "article": elem['supplierArticle'] + "/" + elem['techSize'],
                    "size": elem['techSize'],
                    "count": 1
                }
            elif len(elem['barcode']):
                barcode_dict[elem['barcode']]['count'] += 1

        self.__orders_dict[day] = barcode_dict

    def get_barcodes(self):
        barcode_list = set()
        for date, barcodes in self.__orders_dict.items():
            for barcode in barcodes.keys():
                barcode_list.add(barcode)
        return barcode_list

    def create_table(self):
        table = [(*self.__table_head, *self.__days)]  # Результирующая таблица
        barcode_list = self.get_barcodes()

        for bar in barcode_list:
            ins = [0] * (5 + len(self.__days))
            ins[0] = bar
            table.append(ins)

        # Список всех найденных баркодов
        for row in table:
            day_column = 5
            for date, day_orders in self.__orders_dict.items():
                for barcode, val in day_orders.items():
                    if row[0] == barcode:
                        row[1] = val['nmId']
                        row[2] = val['category']
                        row[3] = val['article']
                        row[4] = val['size']
                        row[day_column] = val['count']
                        continue
                day_column += 1
        return table


if __name__ == '__main__':
    order = OrdersByBarcode(3)
    res = order.execute()
    print(res)
