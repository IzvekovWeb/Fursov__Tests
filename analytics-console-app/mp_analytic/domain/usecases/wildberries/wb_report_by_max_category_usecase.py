from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_report_by_max_category import ReportMaxCategory

WHITE_HTML_COLOR = '#ffffff'


class ReportMaxCategoryUseCase:
    """
        Отчет "Макс Категории"
        """

    def __init__(self):
        self.table = None

    def execute(self):
        title = SHEETS['max_categories']['title']
        sheet_id = SHEETS['max_categories']['id']

        self.table = GoogleSheetAPI(title, SPREADSHEET_ID_SECOND, sheet_id)
        category_list = self.google_sheets_operate()

        response = ReportMaxCategory(category_list).execute()

        self.table.clear(start_column='B')
        self.table.insert(response, start_column='B')

        return self.table.get_sheet_url()

    def google_sheets_operate(self):
        # Get categories
        categories = self.table.get_column('A')
        categories[0].pop(0)

        return categories[0]


if __name__ == '__main__':
    ReportMaxCategoryUseCase().execute()
