from application.utils.utils import print_menu
from domain.usecases.ozon.ozon_dymanic_count_usecase import OzonDynamicCountUseCase
from domain.usecases.ozon.ozon_dynamic_rub_usecase import OzonDynamicRubUseCase


class OzonController:
    """
    Ozon controller with menu
    """

    def __init__(self):
        self.__menu = ["1. Динамика (шт)", "2. Динамика (руб)", "0. Выход"]

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
        Conditional menu for ozon
        :param x: choice
        :return: url to the table
        """
        if x == 1:
            url = OzonDynamicCountUseCase().execute()
        elif x == 2:
            url = OzonDynamicRubUseCase().execute()
        elif x == 0:
            return False
        else:
            print("Некорректный ввод")
            return True
        print(f"Отчет доступен по ссылке: {url}")
        return True
