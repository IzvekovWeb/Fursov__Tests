from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_report_sell_percent import SellPercentReport
from data.utils.functions import update_at
from domain.utils.wb_collect_self_sell_data import collect_self_sell


class SellPercentReportUseCase:
    """
    Отчет "Процент выкупа"
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.update_at = None

    def execute(self) -> str:
        suppliers = self.kwargs.get("suppliers")

        spreadsheet_id = self.kwargs.get("Wildberries 2")

        sheet_title_color = "Выкуп (цвет)"
        sheet_title_subject = "Выкуп (предмет)"
        sheet_title_article = "Выкуп (артикул)"
        sheet_title_size = "Выкуп (размер)"

        sheet_id = self.kwargs.get(sheet_title_color)

        table = GoogleSheetAPI(sheet_title_color, spreadsheet_id, sheet_id)

        table.clear()
        table.clear(sheet_name=sheet_title_subject)
        table.clear(sheet_name=sheet_title_article)
        table.clear(sheet_name=sheet_title_size)

        self_sell_response = collect_self_sell(self.kwargs.get("user_id"))

        response = SellPercentReport(suppliers=suppliers, self_sell_response=self_sell_response).execute()

        table.insert(response[0])
        update_at(response[0], table.insert)

        table.insert(response[1], sheet_name=sheet_title_subject)
        update_at(response[1], table.insert, sheet_name=sheet_title_subject)

        table.insert(response[2], sheet_name=sheet_title_article)
        update_at(response[2], table.insert, sheet_name=sheet_title_article)

        table.insert(response[3], sheet_name=sheet_title_size)
        self.update_at = update_at(response[3], table.insert, sheet_name=sheet_title_size)

        return self.update_at
