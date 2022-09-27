import datetime

from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.utils.functions import form_days, lug_rub_, div_length_, dynamic, div_percent_, date_to_point_format, \
    get_data_from_consolidated_table
from domain.utils.functions import get_suppliers_list


class WeeklyReport:
    def __init__(self, wb_token, days_count, suppliers=None):
        self.__wb_token = wb_token
        self.__suppliers = get_suppliers_list() if suppliers is None else get_suppliers_list(suppliers)
        self.__days = form_days(days_count + 1 if days_count == 1 else days_count, dot_format=1)
        self.__reserve_day = ''

        if days_count == 1:
            date = (datetime.date.today() - datetime.timedelta(2)).strftime('%Y-%m-%d')
            self.__reserve_day = date_to_point_format(date)

        self.__data = {}

    def execute(self, plan: list):
        print('========== ОТЧЕТ "НЕДЕЛЯ" ==========')
        for supplier in self.__suppliers:
            print(f"\rОбрабатываем - {supplier.get('name')}", end=' ')
            data = PersonalAccountAPI.get_consolidated_table(self.__wb_token, supplier.get('supplier-id'))

            for date in self.__days:  # in range of days
                year, month = date.split('.')[2], date.split('.')[1]
                self.__get_data(data, int('20' + year), month, date)

        return self.__get_table(plan)

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

    def __get_table(self, plan):
        table = [('Дата', 'Заказано руб.', 'Заказано шт.', 'Выкупили руб.', 'Выкупили шт.', 'Логистика руб.',
                  'К перечислению', '% выкупа')]
        sum_ordered, sum_goods, sum_payment_rub, sum_payment_piece, sum_logistics, sum_total = 0, 0, 0, 0, 0, 0

        for row in self.__data.values():
            buyback_percent = row.get('paymentSalesRub') / row.get('ordered') if row.get('ordered') else 0
            table.append(
                (row['date'], row['ordered'], row['goodsOrdered'], row['paymentSalesRub'], row['paymentSalesPiece'],
                 row['logisticsCost'], row['totalToTransfer'], buyback_percent))
            if row.get('date') == self.__reserve_day: continue

            sum_total += row['totalToTransfer']
            sum_logistics += row['logisticsCost']
            sum_payment_rub += row['paymentSalesRub']
            sum_payment_piece += row['paymentSalesPiece']
            sum_goods += row['goodsOrdered']
            sum_ordered += row['ordered']

        temp_table = table[1:].copy()

        last = temp_table[len(temp_table) - 1][1:]
        pre_last = temp_table[len(temp_table) - 2][1:]

        while len(table) < 8: table.append(('', '', '', '', '', '', '', '',))  # заполнением пустыми строками

        fact = (sum_ordered, sum_goods, sum_payment_rub, sum_payment_piece, sum_logistics, sum_total,
                sum_payment_rub / sum_ordered if sum_ordered else 0)
        table.append(('Итого',) + fact)
        table.append(('', '', '', '', '', '', '', '',))

        table.append(('Динамика 1 день',) + dynamic(last, pre_last))

        table.append(('', '', '', '', '', '', '', '',))

        if self.__reserve_day:
            table_length = len(temp_table) - 1
        else:
            table_length = len(temp_table)

        plan[-1] = plan[-1] / 100

        table.append(('План',) + tuple(plan))
        table.append(('Факт',) + fact)

        for_daily_plan_length = 7 - table_length if table_length != 7 else 1

        lug_rub = lug_rub_(plan[:-1], fact[:-1])
        table.append(('Отставание $',) + lug_rub)

        lug = div_percent_(lug_rub, plan[:-1])
        table.append(('Отставание',) + lug)

        done = div_percent_(fact[:-1], plan[:-1])
        table.append(('Сделано',) + done)

        plan_today = div_length_(lug_rub, for_daily_plan_length)
        table.append(('План на день',) + plan_today)

        goto_rub = [row / table_length * 7 for row in fact[:-1]]
        table.append(('Идем на $',) + tuple(goto_rub))

        goto = div_percent_(goto_rub, plan)
        table.append(('Идем на',) + tuple(goto))

        return table
