from domain.usecases.wildberries.wb_dynamic_count_usecase import DynamicCountUseCase
from domain.usecases.wildberries.wb_dynamic_rub_usecase import DynamicRubUseCase
from domain.usecases.wildberries.wb_orders_by_barcode_usecase import OrdersByBarcodeUseCase
from domain.usecases.wildberries.wb_orders_by_all_categories_usecase import OrdersByAllCategoriesUseCase
from domain.usecases.wildberries.wb_dynamic_article_count_usecase import DynamicArticleCountUseCase
from domain.usecases.wildberries.wb_dynamic_article_rub_usecase import DynamicArticleRubUseCase
from domain.usecases.wildberries.wb_daily_report_usecase import DailyReportUseCase
from domain.usecases.wildberries.wb_weekly_report_usecase import WeeklyReportUseCase
from domain.usecases.wildberries.wb_monthly_report_usecase import MonthlyReportUseCase
from domain.usecases.wildberries.wb_report_stocks_usecase import StocksUseCase
# from domain.usecases.wildberries.wb_dynamic_by_all_categories_usecase import DynamicByAllCategoriesUseCase
# from domain.usecases.wildberries.wb_dynamic_by_nm_category_usecase import DynamicNMCategoryUseCase
# from domain.usecases.wildberries.wb_report_newly_usecase import OrdersNewlyUseCase
# from domain.usecases.wildberries.wb_report_by_position_usecase import OrdersPositionUseCase
# from domain.usecases.wildberries.wb_report_by_max_category_usecase import ReportMaxCategoryUseCase
# from domain.usecases.wildberries.wb_report_feedback_usecase import FeedbackReportUseCase
# from domain.usecases.wildberries.wb_report_top_usecase import OrdersTopUseCase


class ReportsDRF(object):
    def __init__(self):
        self.__title = {}

    def execute(self):
        self.__run_scripts()

    def get_title_dict(self) -> dict:
        return self.__title

    def __run_scripts(self):
        try:
            self.__title['Динамика заказов поартикульно, шт'] = DynamicCountUseCase()
            self.__title['Динамика заказов поартикульно, руб'] = DynamicRubUseCase()
            self.__title['Динамика заказов по выбранным категориям, руб'] = OrdersByBarcodeUseCase()
            self.__title['Динамика заказов по всем категориям, руб'] = OrdersByAllCategoriesUseCase()
            self.__title['Динамика заказов по основным артикулам, шт'] = DynamicArticleCountUseCase()
            self.__title['Динамика заказов по основным артикулам, руб'] = DynamicArticleRubUseCase()
            self.__title['Ежедневный отчет'] = DailyReportUseCase()
            self.__title['Ежедневный отчет за неделю'] = WeeklyReportUseCase()
            self.__title['Ежедневный отчет за месяц'] = MonthlyReportUseCase()
            self.__title['Отчет по остаткам на складах ВБ'] = StocksUseCase()
            # self.__title['Позиции'] = OrdersPositionUseCase()
            # self.__title['Заказы "топ-500"'] = OrdersTopUseCase()
            # self.__title['Заказы "новинки"'] = OrdersNewlyUseCase()
            # self.__title['Отзывы'] = FeedbackReportUseCase()
            # self.__title['Динамика "категории"'] = DynamicByAllCategoriesUseCase()
            # self.__title['Динамика "категории по номенклатуре"'] = DynamicNMCategoryUseCase()
            # self.__title['Отчет "макс категории"'] = ReportMaxCategoryUseCase()
        except Exception as error:
            print(error)
            return
