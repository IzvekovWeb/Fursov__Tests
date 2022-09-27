from domain.usecases.wildberries.wb_report_stocks_by_regions_usecase import StocksByRegionReportUseCase
from domain.usecases.wildberries.wb_report_stocks_usecase import StocksUseCase
from domain.usecases.wildberries.wb_report_feedback_usecase import FeedbackReportUseCase
from domain.usecases.wildberries.wb_report_top_usecase import OrdersTopUseCase
from domain.usecases.wildberries.wb_report_newly_usecase import OrdersNewlyUseCase
from domain.usecases.wildberries.wb_report_sell_percent_usecase import SellPercentReportUseCase


class OptimalReports(object):
    def __init__(self):
        self.__instances = {}

    def execute(self):
        self.__run_scripts()

    def get_instances_dict(self):
        return self.__instances

    def __run_scripts(self):
        try:
            self.__instances["Остатки"] = StocksUseCase()
            self.__instances["Остатки Регионы"] = StocksByRegionReportUseCase()
            self.__instances["Отзывы"] = FeedbackReportUseCase()
            self.__instances["Топ-500"] = OrdersTopUseCase()
            self.__instances["Новинки"] = OrdersNewlyUseCase()
            # self.__instances["Рентабельность (осн)"] = ProfitabilityArticleUseCase()
            # self.__instances["Рентабельность (титул)"] = ProfitabilityColorUseCase()
            self.__instances["Процент выкупа"] = SellPercentReportUseCase()
        except Exception as error:
            print(error)
            return
