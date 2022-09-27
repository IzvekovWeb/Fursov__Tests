from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_profitability import ProfitabilityReport
from data.repository.wildberries.wb_profitability_article import ProfitabilityArticleReport
from data.repository.wildberries.wb_profitability_object import ProfitabilityObjectReport
from data.utils.functions import update_at
from domain.utils.wb_collect_self_sell_data import collect_self_sell


class ProfitabilityUseCase:
    """
    Отчет "Рентабельность (титул)"
    """

    def __init__(self, kwargs: dict):
        self.kwargs = kwargs

        self.dashboard_data = None
        self.update_at = None
        self.__data = None

    def execute(self):
        suppliers = self.kwargs.get("suppliers")
        spreadsheet_id_logistics = self.kwargs.get("Wildberries Log PC")
        sheet_title_prices = "Себестоимость"
        sheet_id_prices = self.kwargs.get(sheet_title_prices)

        spreadsheet_id = self.kwargs.get("Wildberries 2")
        sheet_title = "Рентабельность (титул)"
        sheet_id = self.kwargs.get(sheet_title)

        row = self.price_formatting(
            GoogleSheetAPI(sheet_title_prices, spreadsheet_id_logistics, sheet_id_prices).get_column('A', 'C')
        )

        self_sell_response = collect_self_sell(self.kwargs.get("user_id"))

        report = ProfitabilityReport(row, suppliers=suppliers, self_sell_response=self_sell_response)
        response, errors = report.execute()

        self.__data = response
        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()

        table.insert(response)

        self.article()
        self.object()

        self.update_at = update_at(response, table.insert)

        self.dashboard_data["baseStat"] = report.get_drf_orders().get("baseStat")

        return self.update_at

    def article(self):
        suppliers = self.kwargs.get("suppliers")
        spreadsheet_id = self.kwargs.get("Wildberries 2")
        sheet_title = "Рентабельность (цвет)"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()
        response = ProfitabilityArticleReport(suppliers=suppliers).execute(self.__data[1:])
        table.insert(response)

    def object(self):
        suppliers = self.kwargs.get("suppliers")
        spreadsheet_id = self.kwargs.get("Wildberries 2")
        sheet_title = "Рентабельность (предмет)"
        sheet_id = self.kwargs.get(sheet_title)

        table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)

        table.clear()
        report = ProfitabilityObjectReport(suppliers=suppliers)
        response = report.execute(self.__data[1:])

        self.dashboard_data = report.get_drf_orders()

        table.insert(response)

    def price_formatting(self, price):
        price[0].pop(0)
        price[1].pop(0)
        price[2].pop(0)
        result = {}
        if len(price[2]) < len(price[0]) and len(price[2]) < 5:
            result = {price[0][i]: int(price[1][i]) if price[1][i] else '-' for i in range(0, len(price[0]))}
        else:
            for i in range(0, len(price[2])):
                if price[2][i].isdigit():
                    if price[1][i]:
                        result[int(price[2][i])] = int(price[1][i])
                    else:
                        result[int(price[2][i])] = '-'
        return result
