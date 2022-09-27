from application.controllers.sell_percent import SellPercentController
from application.utils.utils import print_menu
from domain.usecases.wildberries.wb_abc_usecase import ABCUseCase
from domain.usecases.wildberries.wb_daily_report_usecase import DailyReportUseCase
from domain.usecases.wildberries.wb_dispatch_usecase import DispatchUseCase
from domain.usecases.wildberries.wb_dynamic_article_count_usecase import DynamicArticleCountUseCase
from domain.usecases.wildberries.wb_dynamic_by_all_categories_usecase import DynamicByAllCategoriesUseCase
from domain.usecases.wildberries.wb_dynamic_by_nm_category_usecase import DynamicNMCategoryUseCase
from domain.usecases.wildberries.wb_liquidity_usecase import LiquidityUseCase
from domain.usecases.wildberries.wb_monthly_report_usecase import MonthlyReportUseCase
from domain.usecases.wildberries.wb_report_newly_usecase import OrdersNewlyUseCase
from domain.usecases.wildberries.wb_nomenclatures_usecase import NomenclaturesUseCase
from domain.usecases.wildberries.wb_op_every_day_report_usecase import OPreportUseCase
from domain.usecases.wildberries.wb_dynamic_orders_usecase import DynamicOrdersUseCase
from domain.usecases.wildberries.wb_dynamic_article_rub_usecase import DynamicArticleRubUseCase
from domain.usecases.wildberries.wb_report_by_position_usecase import OrdersPositionUseCase
from domain.usecases.wildberries.wb_profitability_usecase import ProfitabilityUseCase
from domain.usecases.wildberries.wb_report_by_max_category_usecase import ReportMaxCategoryUseCase
from domain.usecases.wildberries.wb_report_stocks_by_regions_usecase import StocksByRegionReportUseCase
from domain.usecases.wildberries.wb_report_stocks_usecase import StocksUseCase
from domain.usecases.wildberries.wb_report_feedback_usecase import FeedbackReportUseCase
from domain.usecases.wildberries.wb_report_top_usecase import OrdersTopUseCase
from domain.usecases.wildberries.wb_orders_by_all_categories_usecase import OrdersByAllCategoriesUseCase
from domain.usecases.wildberries.wb_orders_by_barcode_usecase import OrdersByBarcodeUseCase
from domain.usecases.wildberries.wb_trand_report_usecase import TrandUseCase
from domain.usecases.wildberries.wb_weekly_report_usecase import WeeklyReportUseCase
from domain.usecases.wildberries.wb_position_hourly_usecase import PositionHourlyUseCase
from domain.usecases.wildberries.wb_dispatch_by_region_usecase import DispatchByRegionUseCase

class WildberriesController:
    """
    Wildberries controller with menu
    """

    def __init__(self):
        self.__menu = ["1. Отчет по позициям", "2. Отчет по остаткам", "3. Отчет за день", "4. Отчет за неделю",
                       "5. Отчет за месяц", "6. Заказы (все)", "7. Заказы (топ-500)", "8. Заказы (новинки)",
                       "9. Заказы (все категории)", "10. Заказы по товарам (кол-во)", "11. Заказы по товарам (руб)",
                       "12. Отчеты по рентабельности", "13. Отчет по отзывам", "14. Заказы по артикулам (шт)",
                       "15. Заказы по артикулам (руб)", "16. Динамика категории (ежечас)", "17. ЧП ежедневный",
                       "18. Процент выкупа", "19. Категории", "20. Макс категории", "21. Отгрузка",
                       "22. Отгрузка по региону",
                       "23. Перечень номенклатур", "24. Остатки Регионы", "25. Тренды", "26. ABC", "27. Ликвидность",
                       "28. Позиции Ежечасно",
                       "0. Выход"]

    def start(self):
        """
        class entry point
        :return: result of menu method executing
        """
        self.print_menu()
        x = input("Введите значение: ")

        if not x.isdecimal():
            print("Введите число!")
            return True

        x = int(x)
        if x == 0: return False

        return self.menu(x)

    def print_menu(self):
        """
        print menu
        :return:
        """
        print_menu(self.__menu)

    def menu(self, x: int):
        """
        Conditional menu for wildberries
        :param x: choice
        :return: url to the table
        """
        if x == 1:
            url = OrdersPositionUseCase().execute()  # отчет по позициям
        elif x == 2:
            url = StocksUseCase().execute()  # отчет по остаткам
        elif x == 3:
            url = DailyReportUseCase().execute()  # день
        elif x == 4:
            url = WeeklyReportUseCase().execute()  # неделя
        elif x == 5:
            url = MonthlyReportUseCase().execute()  # месяц
        elif x == 6:
            url = OrdersByBarcodeUseCase().execute()  # заказы (все)
        elif x == 7:
            url = OrdersTopUseCase().execute()  # заказы (топ-500)
        elif x == 8:
            url = OrdersNewlyUseCase().execute()  # заказы новинки
        elif x == 9:
            url = OrdersByAllCategoriesUseCase().execute()  # заказы (все категории)
        elif x == 10:
            url = DynamicOrdersUseCase().execute()  # заказы по товарам (шт.)
        elif x == 11:
            url = DynamicOrdersUseCase().execute()  # заказы по товарам (руб)
        elif x == 12:
            url = ProfitabilityUseCase().execute()  # рентабельность
        elif x == 13:
            url = FeedbackReportUseCase().execute()  # отзывы
        elif x == 14:
            url = DynamicArticleCountUseCase().execute()  # Динамика арт (шт)
        elif x == 15:
            url = DynamicArticleRubUseCase().execute()  # Динамика арт (руб)
        elif x == 16:
            url = DynamicByAllCategoriesUseCase().execute()  # Динамика (все категории)
        elif x == 17:
            url = OPreportUseCase().execute()  # ЧП
        elif x == 18:
            url = SellPercentController().start()  # % выкупа
        elif x == 19:
            url = DynamicNMCategoryUseCase().execute()  # Динамика категорий по номенклатуре
        elif x == 20:
            url = ReportMaxCategoryUseCase().execute()  # Отчет макс категорий
        elif x == 21:
            url = DispatchUseCase().execute()  # Отгрузка
        elif x == 22:
            url = NomenclaturesUseCase().execute()  # Перечень номенклатур
        elif x == 23:
            url = StocksByRegionReportUseCase().execute()  # Остатки Регионы
        elif x == 24:
            url = TrandUseCase().execute()  # Тренды
        elif x == 25:
            url = ABCUseCase().execute()  # ABC
        elif x == 26:
            url = LiquidityUseCase().execute()  # Ликвидность
        elif x == 27:
            url = PositionHourlyUseCase().execute()
        elif x == 28:
            url = DispatchByRegionUseCase().execute()
        elif x == 0:
            return False
        else:
            print("Некорректный ввод")
            return True
        print(f"Отчет доступен по ссылке: {url}")
        return True
