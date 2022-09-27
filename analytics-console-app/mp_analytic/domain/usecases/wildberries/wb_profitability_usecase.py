from config.constants import WB_TOKEN
from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_profitability import ProfitabilityReport
from data.repository.wildberries.wb_profitability_article import ProfitabilityArticleReport
from data.repository.wildberries.wb_profitability_color import ProfitabilityColorReport
from data.repository.wildberries.wb_profitability_object import ProfitabilityObjectReport


class ProfitabilityUseCase:
    """
    Отчет "Рентабельность (титул)"
    """

    def __init__(self):
        self.__data = None

    def execute(self):
        sheet_title_prices = SHEETS.get('prices').get('title')
        sheet_id_prices = SHEETS.get('prices').get('id')

        row = self.price_formatting(
            GoogleSheetAPI(sheet_title_prices, SPREADSHEET_ID_SECOND, sheet_id_prices).get_column('A', 'B'))
        response, errors = ProfitabilityReport(WB_TOKEN, row).execute()
        self.__data = response

        sheet_title = SHEETS.get('profitability').get('title')
        sheet_id = SHEETS.get('profitability').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)
        table.clear()
        table.insert(response)
        self.errors(errors)
        self.article()
        self.color()
        self.object()
        return table.get_sheet_url()

    def article(self):
        sheet_title = SHEETS.get('profitability_article').get('title')
        sheet_id = SHEETS.get('profitability_article').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)
        table.clear()
        response = ProfitabilityArticleReport().execute(self.__data[1:])
        table.insert(response)

    def errors(self, errors):
        sheet_title_err = SHEETS.get('profitability_errors').get('title')
        sheet_id_err = SHEETS.get('profitability_errors').get('id')

        table_error = GoogleSheetAPI(sheet_title_err, SPREADSHEET_ID_SECOND, sheet_id_err)
        table_error.clear()
        table_error.insert(errors)

    def color(self):
        sheet_title = SHEETS.get('profitability_color').get('title')
        sheet_id = SHEETS.get('profitability_color').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)
        table.clear()
        response = ProfitabilityColorReport().execute(self.__data[1:])
        table.insert(response)

    def object(self):
        sheet_title = SHEETS.get('profitability_object').get('title')
        sheet_id = SHEETS.get('profitability_object').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)
        table.clear()
        response = ProfitabilityObjectReport().execute(self.__data[1:])
        table.insert(response)

    def price_formatting(self, price):
        return {price[0][i]: int(float(price[1][i])) if price[1][i] else '-' for i in range(1, len(price[0]))}
