from config.sheets import SHEETS, SPREADSHEET_ID_SECOND, SPREADSHEET_ID_LOGISTICS
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_op_every_day_report import OPeveryDayReport
from data.utils.functions import form_period_days


class OPreportUseCase:
    """
    Отчет ОП
    """

    def __init__(self):
        self.table = None

    def execute(self) -> str:
        days = self.input_dates()

        report = OPeveryDayReport(days)
        response = report.execute()

        logistics_sheet_title = SHEETS.get('logistics').get('title')
        logistics_sheet_id = SHEETS.get('logistics').get('id')

        # Table to operate with logistics and prime cost of item
        self.table = GoogleSheetAPI(logistics_sheet_title, SPREADSHEET_ID_LOGISTICS, logistics_sheet_id)
        self.google_sheets_operate(response, days)

        result_table = report.create_table(response)
        second_op_table_insert = report.create_op_table()

        # Result table
        op_sheet_title = SHEETS.get('profit').get('title')
        op_sheet_id = SHEETS.get('profit').get('id')

        op_table = GoogleSheetAPI(op_sheet_title, SPREADSHEET_ID_SECOND, op_sheet_id)

        op_table.clear()
        op_table.insert(result_table)

        # Second Result table
        second_op_sheet_title = SHEETS.get('op_ev_day').get('title')
        second_op_sheet_id = SHEETS.get('op_ev_day').get('id')

        second_op_table = GoogleSheetAPI(second_op_sheet_title, SPREADSHEET_ID_SECOND, second_op_sheet_id)

        second_op_table.clear()
        second_op_table.insert(second_op_table_insert)

        return f'{op_table.get_sheet_url()}\n{second_op_table.get_sheet_url()}'

    def google_sheets_operate(self, response, days):
        cost_sheet_title = SHEETS.get('prime_cost').get('title')

        percent_sheet_title = SHEETS.get('percent_subject').get('title')
        percent_sheet_id = SHEETS.get('percent_subject').get('id')

        wildberries2table = GoogleSheetAPI(percent_sheet_title, SPREADSHEET_ID_SECOND, percent_sheet_id)
        # Get Categories
        percent_categories = wildberries2table.get_column('A')
        # Get Sell's percentage
        percent_of_sell = wildberries2table.get_column('G')
        percent_categories[0].pop(0)
        percent_of_sell[0].pop(0)

        # Get Categories
        categories = self.table.get_column('B')
        # Get Transition's cost
        transition = self.table.get_column('D')
        categories[0].pop(0)
        transition[0].pop(0)

        # Get Articles
        article_list = self.table.get_column('A', sheet_name=cost_sheet_title)
        # Get article's prime cost
        article_cost_list = self.table.get_column('B', sheet_name=cost_sheet_title)
        article_list[0].pop(0)
        article_cost_list[0].pop(0)

        for day in days:
            for category in response[day].keys():
                category_item = category.split('/')[1]
                try:
                    idx = categories[0].index(category_item)
                    transition_cost = transition[0][idx]
                    response[day][category]['transition'] = int(transition_cost)
                    for article, orders_count in response[day][category]['article'].items():
                        try:
                            idx_art = article_list[0].index(article)
                            prime_cost = article_cost_list[0][idx_art]
                            response[day][category]['prime_cost'] += int(prime_cost) * orders_count
                        except ValueError:
                            continue
                    idx_percent = percent_categories[0].index(category_item)
                    total_percent = percent_of_sell[0][idx_percent]
                    total_percent = float(total_percent.replace(",", "."))
                    response[day][category]['percentage'] += total_percent
                except ValueError as err:
                    print(f"---------- {err}")
                    continue

    def input_dates(self) -> list:
        while True:
            print('Введите даты в формате ГГГГ-ММ-ДД:\n')
            date_from = str(input('С какого числа:\n'))
            date_to = str(input('До какого числа:\n'))
            try:
                days = form_period_days(date_from, date_to)
                return days
            except Exception:
                print('\nПовторите ввод:')
                continue


if __name__ == '__main__':
    OPreportUseCase().execute()
