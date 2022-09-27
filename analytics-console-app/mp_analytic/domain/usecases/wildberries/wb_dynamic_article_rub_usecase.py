from config.constants import WB_TOKEN
from config.sheets import SHEETS, SPREADSHEET_ID
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_dynamic_article_rub import DynamicArticleRubReport


class DynamicArticleRubUseCase:
    """
    Отчет "Заказы по артикулам (руб)"
    """

    def __init__(self):
        self.__sheet_title = SHEETS.get('dynamic_art_rub').get('title')
        self.__sheet_id = SHEETS.get('dynamic_art_rub').get('id')

        self.__table = GoogleSheetAPI(self.__sheet_title, SPREADSHEET_ID, self.__sheet_id)

    def execute(self) -> str:
        response = DynamicArticleRubReport(WB_TOKEN).execute()

        self.__table.clear()
        self.__table.insert(response)
        self.design(len(response))
        return self.__table.get_sheet_url()

    def design(self, length):
        self.__table.number_format(1, length, 5, 13)


if __name__ == '__main__':
    DynamicArticleRubUseCase().execute()
