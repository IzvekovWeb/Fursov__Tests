from config.constants import WB_TOKEN
from config.color_constants import *
from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.get_body_methods.get_body import get_body_dynamic_color
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dynamic_by_nm_category import DynamicByNomenclatureCategory


class DynamicNMCategoryUseCase:
    """
        Отчет "Категории"
        """

    def __init__(self):
        self.table = None

    def execute(self, days_count=7):
        title = SHEETS['categories']['title']
        sheet_id = SHEETS['categories']['id']

        self.table = GoogleSheetAPI(title, SPREADSHEET_ID_SECOND, sheet_id)
        nomenclature_list = self.google_sheets_operate()

        response = DynamicByNomenclatureCategory(nomenclature_list=nomenclature_list, day_count=days_count,
                                                 wb_token=WB_TOKEN).execute()

        self.table.clear(start_column='B')
        self.table.insert(response, start_column='B')
        self.__clear_color()
        self.__color_table(sheet_id)

        return self.table.get_sheet_url()

    def google_sheets_operate(self):
        # Get nomenclatures
        nomenclatures = self.table.get_column('A')

        nomenclatures[0].pop(0)
        not_valid = []
        for i in range(len(nomenclatures[0])):
            try:
                nomenclatures[0][i] = int(nomenclatures[0][i])
            except ValueError:
                not_valid.append(i)
        for invalid in not_valid:
            nomenclatures[0].pop(invalid)

        return nomenclatures[0]

    def __color_table(self, sheet_id):

        body = {"requests": []}
        data_columns = self.__get_last_columns()
        for col in range(len(data_columns) - 1):
            for row in range(len(data_columns[col])):
                if not data_columns[col][row].isdigit():
                    continue
                else:
                    if int(data_columns[col][row]) > int(data_columns[col + 1][row]):
                        get_body_dynamic_color(body,
                                               sheet_id=sheet_id,
                                               start_row=row + 1,
                                               end_row=row + 2,
                                               start_col=col + 11,
                                               end_col=col + 12,
                                               color_cell=RED_LIGHT,
                                               color_headers=GRAY_HEADERS,
                                               )
                    elif int(data_columns[col][row]) < int(data_columns[col + 1][row]):
                        get_body_dynamic_color(body,
                                               sheet_id=sheet_id,
                                               start_row=row + 1,
                                               end_row=row + 2,
                                               start_col=col + 11,
                                               end_col=col + 12,
                                               color_cell=GREEN_LIGHT,
                                               color_headers=GRAY_HEADERS,
                                               )
        self.table.colorize_dynamic(body)

    def __clear_color(self):
        self.table.colorize_row()

    def __get_last_columns(self):
        _data = self.table.get_column('K', 'M')
        for column in range(len(_data)):
            _data[column].pop(0)
        return _data


if __name__ == '__main__':
    DynamicNMCategoryUseCase().execute()
