from domain.usecases.wildberries.wb_daily_report_usecase import DailyReportUseCase
from domain.usecases.wildberries.wb_dynamic_article_count_usecase import DynamicArticleCountUseCase
from domain.usecases.wildberries.wb_dynamic_article_rub_usecase import DynamicArticleRubUseCase
from domain.usecases.wildberries.wb_dynamic_by_all_categories_usecase import DynamicByAllCategoriesUseCase
from domain.usecases.wildberries.wb_dynamic_by_nm_category_usecase import DynamicNMCategoryUseCase
from domain.usecases.wildberries.wb_dynamic_orders_usecase import DynamicOrdersUseCase
from domain.usecases.wildberries.wb_monthly_report_usecase import MonthlyReportUseCase
from domain.usecases.wildberries.wb_report_newly_usecase import OrdersNewlyUseCase
from domain.usecases.wildberries.wb_orders_by_all_categories_usecase import OrdersByAllCategoriesUseCase
from domain.usecases.wildberries.wb_orders_by_barcode_usecase import OrdersByBarcodeUseCase
from domain.usecases.wildberries.wb_report_by_position_usecase import OrdersPositionUseCase
from domain.usecases.wildberries.wb_report_by_max_category_usecase import ReportMaxCategoryUseCase
from domain.usecases.wildberries.wb_report_feedback_usecase import FeedbackReportUseCase
from domain.usecases.wildberries.wb_report_stocks_usecase import StocksUseCase
from domain.usecases.wildberries.wb_report_top_usecase import OrdersTopUseCase
from domain.usecases.wildberries.wb_weekly_report_usecase import WeeklyReportUseCase


class AllEveryDayReportsRun(object):
    def __init__(self):
        self.__urls = {}

    def execute(self):
        self.run_scripts()
        print()
        self.print_urls()

    def get_urls_dict(self):
        return self.__urls

    def print_urls(self):
        for title, url in self.__urls.items():
            print(f'{title} ---> {url}\n')

    def run_scripts(self):
        try:
            self.__urls['Позиции'] = OrdersPositionUseCase().execute()
            self.__urls['Остатки'] = StocksUseCase().execute()
            self.__urls['Отчет за день'] = DailyReportUseCase().execute()
            self.__urls['Отчет за неделю'] = WeeklyReportUseCase().execute()
            self.__urls['Отчет за месяц'] = MonthlyReportUseCase().execute()
            self.__urls['Заказы "все"'] = OrdersByBarcodeUseCase().execute()
            self.__urls['Заказы "топ-500"'] = OrdersTopUseCase().execute()
            self.__urls['Заказы "новинки"'] = OrdersNewlyUseCase().execute()
            self.__urls['Заказы "все категории"'] = OrdersByAllCategoriesUseCase().execute()
            self.__urls['Заказы по товарам "шт"'] = DynamicOrdersUseCase().execute()
            self.__urls['Отзывы'] = FeedbackReportUseCase().execute()
            self.__urls['Динамика по артикулу "шт"'] = DynamicArticleCountUseCase().execute()
            self.__urls['Динамика по артикулу "руб"'] = DynamicArticleRubUseCase().execute()
            self.__urls['Динамика "категории"'] = DynamicByAllCategoriesUseCase().execute()
            self.__urls['Динамика "категории по номенклатуре"'] = DynamicNMCategoryUseCase().execute()
            self.__urls['Отчет "макс категории"'] = ReportMaxCategoryUseCase().execute()
        except Exception as error:
            print(error)
            return
