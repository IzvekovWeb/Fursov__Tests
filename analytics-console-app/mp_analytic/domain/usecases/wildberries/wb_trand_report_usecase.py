from config.sheets import SHEETS, SPREADSHEET_ID, SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_trand_report import OrdersAllCategories


class TrandUseCase:
    """
        Отчет "Тренд"
        """

    def __init__(self):
        self.table = None

    def execute(self, days_count=7):
        title_insert = SHEETS['trand']['title']
        sheet_id_insert = SHEETS['trand']['id']

        self.table = GoogleSheetAPI(title_insert, SPREADSHEET_ID_SECOND, sheet_id_insert)
        category_list = self.google_sheets_operate()

        response = OrdersAllCategories(category_list=category_list, day_count=days_count).execute_mpstats()
        self.google_sheets_operate()
        self.table.clear()
        self.table.insert(response)
        return self.borders(response)

    def borders(self, response):
        row_columns_index = [0, len(response), 0, 9]
        self.table.borders(*row_columns_index, style='SOLID_THICK')
        self.table.borders(0, len(response), 0, 1, style='SOLID_THICK')
        for i in range(0, len(response), 4):
            if len(row_columns_index) == 4:
                row_columns_index.pop(0)
                row_columns_index.pop(0)
            if i == 0:
                self.table.borders(0, 1, 0, 9, style='SOLID_THICK')
            elif i % 4 == 0 and i % 8 != 0:
                row_columns_index.insert(0, i + 1)
            elif i % 8 == 0:
                row_columns_index.insert(1, i + 1)
                self.table.borders(*row_columns_index, style='SOLID_THICK')
        self.table.conditional_color_format(0, 1)

    def google_sheets_operate(self):
        title = SHEETS['category_wb']['title']
        sheet_id = SHEETS['category_wb']['id']
        category_table = GoogleSheetAPI(title, SPREADSHEET_ID, sheet_id)
        category_list = category_table.get_column('B')
        category_list[0].pop(0)
        return category_list[0]


if __name__ == '__main__':
    TrandUseCase().execute()
