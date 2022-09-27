import datetime

from config.constants import WB_TOKEN
from config.sheets import SPREADSHEET_ID
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.utils.functions import form_days, lug_rub_, div_, div_length_, dynamic, get_data_from_consolidated_table, \
    form_days_start_date
from domain.utils.functions import get_suppliers_list

MONTHS = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


class MonthlyReport:
    def __init__(self, wb_token, days_count, suppliers=None):
        self.__wb_token = wb_token
        self.__suppliers = get_suppliers_list() if suppliers is None else get_suppliers_list(suppliers)

        self.__reserve_week = []

        self.__days = form_days(days_count, dot_format=1)
        if len(self.__days) < 8:
            days_count_reserve = 8 - days_count
            self.__reserve_week = form_days_start_date(days_count_reserve, dot_format=1, start_date=self.__days[0])
            self.__days = self.__reserve_week + self.__days

        self.__data = {}

    def execute(self, plan: list):
        print('========== ОТЧЕТ "МЕСЯЦ" ==========')
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

    def __get_table(self, plan: list):
        table = [('Дата', 'Заказано руб.', 'Заказано шт.', 'Выкупили руб.', 'Выкупили шт.', 'Логистика руб.',
                  'К перечислению', '% выкупа')]

        sum_ordered, sum_goods, sum_payment_rub, sum_payment_piece, sum_logistics, sum_total = 0, 0, 0, 0, 0, 0

        for row in self.__data.values():
            buyback_percent = row.get('paymentSalesRub') / row.get('ordered') if row.get('ordered') else 0

            table.append((row['date'], row['ordered'], row['goodsOrdered'], row['paymentSalesRub'],
                          row['paymentSalesPiece'], row['logisticsCost'], row['totalToTransfer'],
                          buyback_percent))

            if row.get('date') in self.__reserve_week: continue

            sum_total += row['totalToTransfer']
            sum_logistics += row['logisticsCost']
            sum_payment_rub += row['paymentSalesRub']
            sum_payment_piece += row['paymentSalesPiece']
            sum_goods += row['goodsOrdered']
            sum_ordered += row['ordered']

        temp_table = table[1:].copy()

        last = temp_table[len(temp_table) - 1][1:]
        pre_last = temp_table[len(temp_table) - 2][1:]

        week_dynamic_data = temp_table[len(temp_table) - 8][1:]

        if self.__reserve_week:
            days_length = len(temp_table[len(self.__reserve_week):])
        else:
            days_length = len(temp_table)

        fact = [sum_ordered, sum_goods, sum_payment_rub, sum_payment_piece, sum_logistics, sum_total,
                sum_payment_rub / sum_ordered if sum_ordered else 0]
        table.append(('Итого',) + tuple(fact))

        table.append(('', '', '', '', '', '', '', '',))

        table.append(('Динамика 1 день',) + dynamic(last, pre_last))
        table.append(('Динамика 7 дней',) + dynamic(last, week_dynamic_data))

        table.append(('', '', '', '', '', '', '', '',))

        plan[-1] = plan[-1] / 100

        table.append(('План',) + tuple(plan))
        table.append(('Факт',) + tuple(fact))

        lug_rub = lug_rub_(plan[:-1], fact[:-1])
        table.append(('Отставание $',) + lug_rub)

        lug = div_(lug_rub, plan)
        table.append(('Отставание',) + lug)

        done = div_(fact[:-1], plan[:-1])
        table.append(('Сделано',) + done)

        length = MONTHS[datetime.date.today().month] - days_length if days_length < MONTHS[
            datetime.date.today().month] else 1
        plan_today = div_length_(lug_rub, length)
        table.append(('План на день',) + plan_today)

        # СРЕДНЕЕ ЗНАЧЕНИЕ ПОСЛЕДНИХ 7 ДНЕЙ * НА ОСТАТОК ДНЕЙ МЕСЯЦА, ВКЛЮЧАЯ СЕГОДНЯ + ИТОГО
        week = temp_table[-7:]

        months_day = MONTHS[datetime.date.today().month] - days_length
        if not months_day:
            goto_rub = fact
        else:
            week_data = [sum_col_list(i, week) / 7 * months_day for i in range(1, len(week) + 1)]
            goto_rub = [week_data[i] + fact[i] for i in range(len(week_data))]

        table.append(('Идем на $',) + tuple(goto_rub[:-1]))

        goto = []
        for row in range(len(goto_rub)):
            goto.append(goto_rub[row] / plan[row])
        table.append(('Идем на',) + tuple(goto[:-1]))

        return table


def sum_col_list(index, data):
    suma = 0
    for i in data:
        suma += i[index]
    return suma


if __name__ == '__main__':
    row = GoogleSheetAPI("План", SPREADSHEET_ID, "156321916").get_row(4)[0]
    plan = [int(i) for i in row]
    response = MonthlyReport(WB_TOKEN, 22).execute(plan)
