from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_op_every_day_report import OPeveryDayReport
from data.utils.functions import update_at, form_days_start_date


class OPreportUseCase:
    """
    Отчет ОП
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.update_at = None

    def execute(self) -> str:
        days = form_days_start_date(7)

        suppliers = self.kwargs.get("suppliers")

        spreadsheet_id_op = self.kwargs.get("Wildberries 2")
        sheet_title_op_more = "ОП подробная"  # Result table
        sheet_id_op_more = self.kwargs.get(sheet_title_op_more)

        sheet_title_op_days = "ОП ежедн"  # Second Result table
        sheet_id_op_days = self.kwargs.get(sheet_title_op_days)

        spreadsheet_id_logistics = self.kwargs.get("Wildberries Log PC")
        sheet_title_logistics = "Логистика"
        sheet_id_logistics = self.kwargs.get(sheet_title_logistics)

        report = OPeveryDayReport(days, suppliers=suppliers)
        response = report.execute()
        # Table to operate with logistics and prime cost of item
        table = GoogleSheetAPI(sheet_title_logistics, spreadsheet_id_logistics, sheet_id_logistics)
        self.google_sheets_operate(table, response, days)

        result_table = report.create_table(response)
        table_insert_op_days = report.create_op_table()
        table_op_more = GoogleSheetAPI(sheet_title_op_more, spreadsheet_id_op, sheet_id_op_more)
        table_op_more.clear()
        table_op_more.insert(result_table)

        table_op_days = GoogleSheetAPI(sheet_title_op_days, spreadsheet_id_op, sheet_id_op_days)
        table_op_days.clear()
        table_op_days.insert(table_insert_op_days)

        self.update_at = update_at(result_table)

        return self.update_at

    def google_sheets_operate(self, table, response, days):
        cost_sheet_title = "Себестоимость"

        spreadsheet_id = self.kwargs.get("Wildberries 2")
        percent_sheet_title = "Выкуп (предмет)"
        percent_sheet_id = self.kwargs.get(percent_sheet_title)

        wildberries2table = GoogleSheetAPI(percent_sheet_title, spreadsheet_id, percent_sheet_id)

        # Get Categories
        percent_categories = wildberries2table.get_column('A')
        # Get Sell's percentage
        percent_of_sell = wildberries2table.get_column('G')
        percent_categories[0].pop(0)
        percent_of_sell[0].pop(0)

        # Get Categories
        categories = table.get_column('A')
        # Get Transition's cost
        transition = table.get_column('B')
        categories[0].pop(0)
        transition[0].pop(0)

        # Get Articles
        article_list = table.get_column('A', sheet_name=cost_sheet_title)
        # Get article's prime cost
        article_cost_list = table.get_column('B', sheet_name=cost_sheet_title)

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
