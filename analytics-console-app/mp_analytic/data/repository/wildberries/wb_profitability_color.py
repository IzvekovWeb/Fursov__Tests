class ProfitabilityColorReport:
    def __init__(self):
        self.__response = {}

    def execute(self, data):
        self.get_data(data)
        return self.__get_table()

    def get_data(self, data):
        for i in data:
            article = i[4]
            quantity = int(i[5])
            op = int(i[10]) if i[10] != '-' else "-"

            if not self.__response.get(article):

                self.__response[article] = {
                    'supplier': i[0],
                    'article': article,
                    'nm_id': i[3],
                    'quantity': quantity,
                    'op': op,
                }
            else:
                if type(op) != str and type(self.__response[article]['op']) != str:
                    self.__response[article]['op'] += op
                elif type(op) != str:
                    self.__response[article]['op'] = op
                self.__response[article]['quantity'] += quantity

    def __get_table(self):
        table = [("Поставщик", "Артикул", "Номенклатура", "Продажи, шт.", "ОП", "Прибыль на 1шт.")]

        for i in self.__response.values():
            op = i['op']
            quantity = i['quantity']
            profit = '-'

            if type(quantity) == int and type(op) == int:
                if quantity != 0:
                    profit = round(op / quantity)
            table.append((i['supplier'], i['article'], i['nm_id'], quantity, op, profit))
        return table
