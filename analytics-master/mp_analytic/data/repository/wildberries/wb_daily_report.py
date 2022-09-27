import datetime

from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.utils.functions import form_days, get_data_from_consolidated_table, date_to_point_format


class DailyReport:
    """
    Отчет "День"
    """

    def __init__(self, days_count, suppliers=None):
        self.__suppliers = suppliers
        self.__data = {}
        self.__days = form_days(days_count + 1, dot_format=1)
        self.__dynamic_week_day = date_to_point_format(
            (datetime.date.today() - datetime.timedelta(8)).strftime("%Y-%m-%d"))

        self.__drf_stat = {}

    def execute(self):
        print('========== ОТЧЕТ "ДЕНЬ" ==========')
        for supplier in self.__suppliers:
            print(f"\rОбрабатываем - {supplier.get('name')}", end=' ')
            data = PersonalAccountAPI.get_consolidated_table(supplier.get('wb_token'), supplier.get('supplier-id'))

            for date in self.__days:  # in range of days
                year, month = date.split('.')[2], date.split('.')[1]
                self.__get_data(data, int('20' + year), month, date)

        return self.__get_table()

    def __get_data(self, data: dict, year: int, month: str, day: str):
        """
        Очистка данных, полученных от Wildberries
        :param data: данные
        :param year: год
        :param month: месяц
        :param day: дата
        :return:
        """
        if not data.get('data'):  # Check if data is not empty
            return

        day_data = get_data_from_consolidated_table(data, year, month, day)  # get one day data from cons. table

        if day_data is None:
            return

        if not self.__data.get(day):  # day not in data
            self.__data[day] = {'date': day, 'ordered': day_data['ordered'],
                                'goodsOrdered': day_data['goodsOrdered'],
                                'paymentSalesRub': day_data['paymentSalesRub'],
                                'paymentSalesPiece': day_data['paymentSalesPiece'],
                                'logisticsCost': day_data['logisticsCost'],
                                'totalToTransfer': day_data['totalToTransfer']}
        else:
            self.__data[day]['ordered'] += day_data['ordered']
            self.__data[day]['goodsOrdered'] += day_data['goodsOrdered']
            self.__data[day]['paymentSalesRub'] += day_data['paymentSalesRub']
            self.__data[day]['paymentSalesPiece'] += day_data['paymentSalesPiece']
            self.__data[day]['logisticsCost'] += day_data['logisticsCost']
            self.__data[day]['totalToTransfer'] += day_data['totalToTransfer']

    def __get_table(self) -> list:
        """
        Формирование таблицы для выгрузки\n
        :return: list - таблица
        """
        table = [('Дата', 'Заказано руб.', 'Заказано шт.', 'Выкупили руб.', 'Выкупили шт.', 'Логистика руб.',
                  'К перечислению', '% выкупа')]

        sum_ordered, sum_goods, sum_payment_rub, sum_payment_piece, sum_logistics, sum_total = 0, 0, 0, 0, 0, 0

        for row in self.__data.values():
            buyback_percent = row.get('paymentSalesRub') / row.get('ordered') if row.get('ordered') else 0

            table.append((row.get('date'), row.get('ordered'), row.get('goodsOrdered'), row.get('paymentSalesRub'),
                          row.get('paymentSalesPiece'), row.get('logisticsCost'), row.get('totalToTransfer'),
                          buyback_percent))

            if row.get('date') == self.__dynamic_week_day: continue

            sum_total += row['totalToTransfer']
            sum_logistics += row['logisticsCost']
            sum_payment_rub += row['paymentSalesRub']
            sum_payment_piece += row['paymentSalesPiece']
            sum_goods += row['goodsOrdered']
            sum_ordered += row['ordered']

        sum_buyback_percent = sum_payment_rub / sum_ordered if sum_ordered else 0

        table.append(("Итого", sum_ordered, sum_goods, sum_payment_rub, sum_payment_piece, sum_logistics, sum_total,
                      sum_buyback_percent))

        table.append(('', '', '', '', '', '', '', '',))
        table.append(('', '', '', '', '', '', '', '',))

        table.append(('Динамика 1 день', '=(B9-B8)/B8', '=(C9-C8)/C8', '=(D9-D8)/D8', '=(E9-E8)/E8', '=(F9-F8)/F8',
                      '=(G9-G8)/G8', '=(H9-H8)/H8'))
        table.append(('Динамика 7 дней', '=(B9-B2)/B2', '=(C9-C2)/C2', '=(D9-D2)/D2', '=(E9-E2)/E2', '=(F9-F2)/F2',
                      '=(G8-G2)/G2', '=(H8-H2)/H2'))

        self.__collect_drf_stat(table)

        return table

    def __collect_drf_stat(self, table):
        rub_inc = (table[8][1] - table[1][1]) / table[1][1] * 100
        rub_inc = round(rub_inc)
        count_inc = (table[8][2] - table[1][2]) / table[1][2] * 100
        count_inc = round(count_inc)
        sells_inc = (table[8][3] - table[1][3]) / table[1][3] * 100
        sells_inc = round(sells_inc)

        self.__drf_stat = {
            "ordersRub": {
                "ordersToday": table[9][1],
                "increase": rub_inc
            },
            "ordersCount": {
                "ordersToday": table[9][2],
                "increase": count_inc
            },
            "sells": {
                "ordersToday": table[9][3],
                "increase": sells_inc
            },
            "baseStat": []
        }
        for i in range(2, 9):
            self.__drf_stat["baseStat"].append({
                "date": table[i][0],
                "data": int(table[i][1])
            })

    def get_drf_stat(self):
        return self.__drf_stat
