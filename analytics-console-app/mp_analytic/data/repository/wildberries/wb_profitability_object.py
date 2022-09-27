class ProfitabilityObjectReport:
    def __init__(self):
        self.__response = {}

    def execute(self, data):
        self.get_data(data)
        return self.__get_table()

    def get_data(self, data):
        for i in data:
            supplier = i[0]
            quantity = i[5]
            subject = i[2]
            op = i[10] if i[10] != '-' else "-"

            if not self.__response.get(subject):

                self.__response[subject] = {
                    'supplier': supplier,
                    'subject': subject,
                    'quantity': quantity,
                    'op': op,
                }
            else:
                if type(op) != str and type(self.__response[subject]['op']) != str:
                    self.__response[subject]['op'] += op
                elif type(op) != str:
                    self.__response[subject]['op'] = op
                self.__response[subject]['quantity'] += quantity

    def __get_table(self):
        table = [("Поставщик", "Предмет", "Продажи, шт.", "ОП", "Прибыль на 1шт.")]

        for i in self.__response.values():
            op = i['op']
            quantity = i['quantity']
            profit = '-'
            if type(quantity) == int and type(op) == int:
                if quantity != 0:
                    profit = round(op / quantity)

            table.append((i['supplier'], i['subject'], quantity, op, profit))
        return table
