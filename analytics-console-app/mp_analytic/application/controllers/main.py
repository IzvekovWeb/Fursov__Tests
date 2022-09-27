from application.controllers.ozon import OzonController
from application.controllers.wildberries import WildberriesController
from application.controllers.wb_all_every_day_reports_run_scripts import AllEveryDayReportsRun
from application.utils.utils import print_menu


class MainController:
    """
    Main Controller class with general loop
    """

    def __init__(self):
        self.__menu = ["1. Wildberries",
                       "2. Wildberries (запуск всех ежедневных отчетов)",
                       "3. Ozon",
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

            result = self.menu(x)
            if not result:
                break

    def menu(self, x: int) -> bool:
        """
        Conditional menu for pro
        :param x:
        :return:
        """
        if x == 1:  # Wildberries
            result = WildberriesController().start()
        elif x == 2:  # Run all reports Wildberries
            result = AllEveryDayReportsRun().execute()
        elif x == 3:
            result = OzonController().start()
        elif x == 0:  # Exit
            result = False
        else:  # Default
            print("Некорректный ввод")
            result = True
        return result

    def print_menu(self):
        print_menu(self.__menu)
