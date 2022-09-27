from config.sheets import SHEETS, SPREADSHEET_ID
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_order_by_position import OrdersPosition
from data.utils.functions import update_at
from domain.utils.valid_list import is_valid_list


class OrdersPositionUseCase:
    """
        Отчет "Позиции"
    """

    def __init__(self):
        self.title = "Позиции"
        self.url = None
        self.update_at = None

    def execute(self):
        title = SHEETS['positions']['title']
        sheet_id = SHEETS['positions']['id']

        table = GoogleSheetAPI(title, SPREADSHEET_ID, sheet_id)
        category_list, nomenclature_list, length_of_rows = self.google_sheets_operate(table)

        response = OrdersPosition(category_list=category_list, nomenclature_list=nomenclature_list).execute()
        length_of_new_data = len(response)

        table.clear(start_column='B')

        self.delete_or_draw_borders(table, length_of_rows)  # Delete BORDERS
        self.delete_or_draw_borders(table, length_of_new_data, 'SOLID_THICK')  # Draw BORDERS

        table.insert(response, start_column='B')

        self.update_at = update_at(response, table.insert)

        self.url = table.get_sheet_url()
        return self.url

    def google_sheets_operate(self, table):
        # Get Categories
        categories = table.get_column('B', sheet_name='Категории')
        nomenclatures = table.get_column('A', sheet_name='Позиции')
        length_of_rows = table.get_column('B', sheet_name='Позиции')

        if not length_of_rows:
            exist_length_of_rows = 0
        else:
            exist_length_of_rows = len(length_of_rows[0])

        categories[0].pop(0)
        nomenclatures[0].pop(0)

        is_valid_list(nomenclatures[0])

        return categories[0], nomenclatures[0], exist_length_of_rows

    def delete_or_draw_borders(self, table, length_of_rows, mode='NONE'):
        """
        Deleting or drawing borders of cells\n
        :param table: Table to operate with
        :param length_of_rows: The number of row to update
        :param mode: 'NONE' - delete border; 'SOLID_THICK' - draw thick border
        :return: None
        """

        table.borders(style=mode, start_column=1, end_column=14,
                      start_row=length_of_rows, end_row=length_of_rows + 1,
                      left=False, right=False, bottom=False)

        table.borders(style=mode, start_column=14,
                      end_column=15, right=False, top=False,
                      end_row=length_of_rows, bottom=False)

        table.borders(style=mode,
                      start_column=0, end_column=1)
