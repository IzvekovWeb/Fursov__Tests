from application.utils.utils import print_menu
from domain.usecases.wildberries.wb_report_sell_percent_usecase import SellPercentReportUseCase
from domain.usecases.wildberries.wb_report_sell_percent_by_color_usecase import SellPercentReportByColorUseCase
from domain.usecases.wildberries.wb_report_sell_percent_by_subject_usecase import SellPercentReportBySubjectUseCase
from domain.usecases.wildberries.wb_report_sell_percent_by_article_usecase import SellPercentReportByArticleUseCase
from domain.usecases.wildberries.wb_report_sell_percent_by_size_usecase import SellPercentReportBySizeUseCase


class SellPercentController:
    """
    Sell Percent Controller class with general loop
    """

    def __init__(self):
        self.__menu = ["1. Собрать все",
                       "2. Артикул/Цвет",
                       "3. Предмет",
                       "4. Артикул",
                       "5. Aртикул/Цвет/Размер",
                       "0. Выход"]

    def start(self):
        """
        entry point
        :return:
        """
        while True:
            self.print_menu()
            x = input("Введите значение: ")

            if not x.isdecimal():
                print("Введите число!")
                continue

            x = int(x)
            if x == 0:
                break

            return self.menu(x)

    def menu(self, x: int) -> str:
        """
        Conditional menu for SellPercent
        :param x:
        :return:
        """

        if x == 1:
            url = SellPercentReportUseCase().execute()

        elif x == 2:
            url = SellPercentReportByColorUseCase().execute()
        elif x == 3:
            url = SellPercentReportBySubjectUseCase().execute()
        elif x == 4:
            url = SellPercentReportByArticleUseCase().execute()
        elif x == 5:
            url = SellPercentReportBySizeUseCase().execute()

        else:  # Default
            print("Некорректный ввод")
            return ''

        return url

    def print_menu(self):
        print_menu(self.__menu)
