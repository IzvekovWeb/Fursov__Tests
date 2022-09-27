from config.color_constants import *
from data.google.get_body_methods.get_body import get_body_colorize
from data.google.get_range_methods.get_range import get_range_colorize
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dynamic_by_all_categories import DynamicAllCategories
from data.utils.functions import update_at


class DynamicByAllCategoriesUseCase:
    """
    Динамика заказов по категориям
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.update_at = None

    def execute(self, days_count: int = 7):
        suppliers = self.kwargs.get("suppliers")
        spreadsheet_id = self.kwargs.get("Wildberries 2")
        sheet_title = "Динамика (категории)"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        categories = self.google_sheets_operate(table)
        if categories == -1:
            return None
        response, overall_row_number = DynamicAllCategories(days_count, categories, suppliers=suppliers).execute()
        length_of_response = len(response)
        width_of_response = len(response[0])

        self.colorize_and_draw_borders(table, overall_row_number, length_of_response, width_of_response)

        table.clear('B')
        table.insert(response, start_column='B')

        self.update_at = update_at(response, table.insert)

        return self.update_at

    def google_sheets_operate(self, table):
        # Get Categories
        categories = table.get_column('A')
        if not categories:
            return -1
        categories[0].pop(0)  # Delete row with name of column

        return categories[0]

    def colorize_and_draw_borders(self, table, overall_row_number, length_of_response, width):
        table.colorize_row()

        _range = get_range_colorize
        _body = get_body_colorize
        body = {"requests": []}

        for row in range(overall_row_number, length_of_response, overall_row_number):
            _body(body, _range(row, row + 1, 1, width + 1, table.sheet_id), OVERALL_CELL_HTML_COLOR)

        table.colorize_row(body)

        table.borders(clear=1)

        table.borders(start_column=1, end_column=2,
                      style='SOLID_THICK', end_row=length_of_response)

        table.borders(start_column=1 + width, end_row=length_of_response,
                      right=False, top=False, bottom=False,
                      style='SOLID_THICK')

        table.borders(start_column=1, end_column=1 + width,
                      style='SOLID_THICK',
                      start_row=length_of_response - 1,
                      end_row=length_of_response)
