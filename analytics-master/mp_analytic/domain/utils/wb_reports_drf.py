from domain.usecases.wildberries.wb_abc_usecase import ABCUseCase
from domain.usecases.wildberries.wb_daily_report_usecase import DailyReportUseCase
from domain.usecases.wildberries.wb_dispatch_usecase import DispatchUseCase
from domain.usecases.wildberries.wb_dynamic_by_all_categories_usecase import DynamicByAllCategoriesUseCase
from domain.usecases.wildberries.wb_orders_by_barcode_usecase import OrdersByBarcodeUseCase
from domain.usecases.wildberries.wb_dynamic_orders_usecase import DynamicOrdersUseCase
from domain.usecases.wildberries.wb_liquidity_usecase import LiquidityUseCase
from domain.usecases.wildberries.wb_monthly_report_usecase import MonthlyReportUseCase
from domain.usecases.wildberries.wb_op_every_day_report_usecase import OPreportUseCase
from domain.usecases.wildberries.wb_orders_by_all_categories_usecase import OrdersByAllCategoriesUseCase
from domain.usecases.wildberries.wb_profitability_usecase import ProfitabilityUseCase
from domain.usecases.wildberries.wb_report_feedback_usecase import FeedbackReportUseCase
from domain.usecases.wildberries.wb_report_sell_percent_usecase import SellPercentReportUseCase
from domain.usecases.wildberries.wb_report_stocks_by_regions_usecase import StocksByRegionReportUseCase
from domain.usecases.wildberries.wb_report_stocks_usecase import StocksUseCase
from domain.usecases.wildberries.wb_report_top_usecase import OrdersTopUseCase
from domain.usecases.wildberries.wb_weekly_report_usecase import WeeklyReportUseCase


class ReportsDRF(object):
    def __init__(self):
        self.__title = {}

    def execute(self):
        self.__run_scripts()

    def get_title_dict(self) -> dict:
        return self.__title

    def __run_scripts(self):
        try:
            self.__title['Ежедневный отчет'] = DailyReportUseCase
            self.__title['Ежедневный отчет за неделю'] = WeeklyReportUseCase
            self.__title['Ежедневный отчет за месяц'] = MonthlyReportUseCase
            self.__title['Динамика заказов поартикульно'] = DynamicOrdersUseCase
            self.__title['Динамика заказов по всем категориям'] = OrdersByAllCategoriesUseCase
            self.__title['Динамика заказов по выбранным категориям'] = OrdersByBarcodeUseCase
            self.__title['Отчет по остаткам на складах ВБ'] = StocksUseCase
            self.__title['Отчет по региональным остаткам'] = StocksByRegionReportUseCase
            self.__title['Категорийная динамика заказов по выбранным sku'] = OrdersTopUseCase
            self.__title['Отчет по отзывам'] = FeedbackReportUseCase
            self.__title['Отчет по отгрузке'] = DispatchUseCase
            self.__title['Ежечасная динамика заказов по категориям'] = DynamicByAllCategoriesUseCase
            self.__title['Ежедневный отчет по ОП'] = OPreportUseCase
            self.__title['Отчет по рентабельности'] = ProfitabilityUseCase
            self.__title['Процент выкупа'] = SellPercentReportUseCase
            self.__title['ABC-анализ'] = ABCUseCase
            self.__title['Фирменный отчет MarketData'] = LiquidityUseCase
        except Exception as error:
            print(error)
            return
