from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI


class PositionHourly:
    """
        Отчет "Позиции Ежечасно"
    """
    def __init__(self, search_query, nomenclature_list):
        self.search_query = search_query
        self.nomenclature_list = nomenclature_list
        self.response = []

    def execute(self):
        self.__get_positions()
        return self.response

    def __get_positions(self):
        self.response.append(["Позиция"])
        for nomenclature in self.nomenclature_list:
            self.response.append((PersonalAccountAPI.get_position(self.search_query, nomenclature), ))
