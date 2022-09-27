from config.color_constants import *
from config.constants import WB_TOKEN
from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.get_body_methods.get_body import get_body_colorize
from data.google.get_range_methods.get_range import get_range_colorize
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dynamic_by_all_categories import DynamicAllCategories


class DynamicByAllCategoriesUseCase:
    """
    Динамика заказов по категориям
    """

    def __init__(self):
        self.table = None

    def execute(self, days_count: int = 7) -> str:
        sheet_title = SHEETS.get('dynamic_categories').get('title')
        sheet_id = SHEETS.get('dynamic_categories').get('id')
        self.table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)

        categories = self.google_sheets_operate()
        response, overall_row_number = DynamicAllCategories(WB_TOKEN, days_count, categories).execute()
        length_of_response = len(response)
        width_of_response = len(response[0])

        self.colorize_and_draw_borders(overall_row_number, length_of_response, width_of_response)

        self.table.clear('B')
        self.table.insert(response, start_column='B')

        return self.table.get_sheet_url()

    def google_sheets_operate(self):
        # Get Categories
        categories = self.table.get_column('A')
        categories[0].pop(0)  # Delete row with name of column

        return categories[0]

    def colorize_and_draw_borders(self, overall_row_number, length_of_response, width):
        self.table.colorize_row()

        _range = get_range_colorize
        _body = get_body_colorize
        body = {"requests": []}

        for row in range(overall_row_number, length_of_response, overall_row_number):
            _body(body, _range(row, row + 1, 1, width + 1, self.table.sheet_id), OVERALL_CELL_HTML_COLOR)
            # self.table.colorize_row(row, row + 1, 1, width + 1, color=OVERALL_CELL_HTML_COLOR)
        self.table.colorize_row(body)

        self.table.borders(clear=1)

        self.table.borders(start_column=1, end_column=2,
                           style='SOLID_THICK', end_row=length_of_response)

        self.table.borders(start_column=1 + width, end_row=length_of_response,
                           right=False, top=False, bottom=False,
                           style='SOLID_THICK')

        self.table.borders(start_column=1, end_column=1 + width,
                           style='SOLID_THICK',
                           start_row=length_of_response - 1,
                           end_row=length_of_response)


if __name__ == '__main__':
    DynamicByAllCategoriesUseCase().execute()
