class ProfitabilityObjectReport:
    def __init__(self, suppliers=None):
        self.__suppliers = suppliers
        self.__drf_orders = {}
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

        top_dict = []
        for i in self.__response.values():
            op = i['op']
            quantity = i['quantity']
            profit = '-'
            if type(quantity) == int and type(op) == int:
                if quantity != 0:
                    profit = round(op / quantity)

            table.append((i['supplier'], i['subject'], quantity, op, profit))

            if isinstance(profit, int):
                top_dict.append((len(table) - 1, profit))

        self.__collect_top_orders(table, top_dict)

        return table

    def __collect_top_orders(self, table: list, top_dict: list):
        self.__drf_orders["topProfit"] = {
            "name": [],
            "data": [],
        }
        self.__drf_orders["worstProfit"] = {
            "name": [],
            "data": [],
        }

        top_dict.sort(key=lambda tup: tup[1], reverse=True)

        if len(top_dict) < 10:
            top_count = len(top_dict)
        else:
            top_count = 10

        for idx in range(top_count):
            row_profit = table[top_dict[idx][0]]
            row_worst = table[top_dict[-(1 + idx)][0]]

            self.__drf_orders["topProfit"]["name"].append(row_profit[1])
            self.__drf_orders["topProfit"]["data"].append(row_profit[-1])

            self.__drf_orders["worstProfit"]["name"].append(row_worst[1])
            self.__drf_orders["worstProfit"]["data"].append(row_worst[-1])

    def get_drf_orders(self):
        return self.__drf_orders
