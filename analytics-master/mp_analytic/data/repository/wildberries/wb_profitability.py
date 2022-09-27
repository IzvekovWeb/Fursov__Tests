from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.marketplaces.wildberries.wb_supplier_stat import SupplierStatAPI


class ProfitabilityReport(object):
    def __init__(self, prices, suppliers=None, weeks=2, self_sell_response=None):
        self.__drf_orders = {}
        self.__suppliers = suppliers
        self.storage_paid = 0
        self.count_sum = 0
        self.weeks = weeks
        self.response = {}
        self.prices = prices
        self.errors = []

        if self_sell_response is None:
            self_sell_response = {}
        self.self_sell_response = self_sell_response

    def execute(self):
        for supplier in self.__suppliers:
            print(f"Обрабатываем поставщика - {supplier.get('name')}")
            self.get_finance_reports_id(supplier)
        return self.__get_table(), self.errors

    def get_finance_reports_id(self, supplier):
        report = []
        responses = PersonalAccountAPI().get_finance_reports_id(supplier.get('wb_token'),
                                                                supplier.get("supplier-id"))
        if isinstance(responses, list):
            responses = responses[0].get("data")[:self.weeks]
            print(f"Получение отчетов для поставщика - {supplier.get('name')}")

            for response in responses:
                self.storage_paid += response.get("paidStorageSum")

                finance_report_id = response.get("id")
                try:
                    finance_report = PersonalAccountAPI().get_weekly_finance_report(supplier.get('wb_token'),
                                                                                    supplier["supplier-id"],
                                                                                    finance_report_id)
                    if not isinstance(finance_report, list):
                        finance_report = []
                    self.get_data(finance_report, supplier.get('name'))
                except ConnectionError:
                    self.get_data_from_api([response["dateFrom"], response["dateTo"]], supplier)
                    print("Working API...")
        return report

    def check_type(self, order_type, count, retail_amount, nomenclature):
        if order_type == 'Продажа' and count == 1:
            self.response[nomenclature]['rub'] += retail_amount
            self.response[nomenclature]['quantity'] += 1
            self.count_sum += 1
        if order_type == 'Возврат' and count == 1:
            self.response[nomenclature]['rub'] -= retail_amount
            self.response[nomenclature]['quantity'] -= 1
            self.count_sum -= 1

    def get_data_from_api(self, dates, supplier):
        finance_report = SupplierStatAPI.report_detail_by_period(supplier, dates)
        for order in finance_report:
            subject = order.get("subject_name") or ""
            article_color = order.get("sa_name") or ""
            brand = order.get("brand_name") or ""
            nomenclature = order.get("nm_id") or ""

            order_type = order.get("doc_type_name")
            count = order.get("quantity")
            retail_amount = order.get("retail_amount")

            if not self.response.get(nomenclature):
                self.response[nomenclature] = {
                    'supplier': supplier.get('name'), 'quantity': 0, 'delivery': 0,
                    'nm_id': nomenclature,
                    'brand': brand, 'subject': subject,
                    'article': article_color, 'rub': 0
                }

            self.check_type(order_type, count, retail_amount, nomenclature)
            self.response[nomenclature]['delivery'] += order.get("delivery_rub")

    def get_data(self, finance_report, supplier_name):
        for order in finance_report:
            nomenclature = order.get("nomenclatureId")
            order_type = order.get("type")
            count = order.get("quantity")
            retail_amount = order.get("retailAmount")

            if not self.response.get(nomenclature):
                self.response[nomenclature] = {
                    'supplier': supplier_name, 'quantity': 0, 'delivery': 0, 'nm_id': nomenclature,
                    'brand': order.get("brand").get("name"), 'subject': order.get("subject").get("name"),
                    'article': order.get("articleSupplier"), 'rub': 0
                }

            self.check_type(order_type, count, retail_amount, nomenclature)
            self.response[nomenclature]['delivery'] += order.get("deliveryRub")

    def __get_table(self):
        if self.count_sum:
            storage = self.storage_paid / self.count_sum
        else:
            storage = 0
        print("Формируется таблица для выгрузки...")
        table = [
            ("Поставщик", "Бренд", "Предмет", "Номенклатура", "Артикул",
             "Продажи, шт.", "Продажи, руб.", "Логистика", "Хранение",
             "Себестоимость", "ОП", "Прибыль на 1шт.")]
        stata = 0
        base_stat = {
            "op": 0,
            "averageProfit": 0,
            "primeCost": 0,
            "storage": 0,
            "logistics": 0,
            "count": 0,
        }
        for order in self.response.values():
            if self.prices.get(order["article"]):
                main_key = order['article']
            else:
                main_key = order['nm_id']

            rub = round(order['rub'])
            quantity = order['quantity']
            delivery = round(order['delivery'])
            order_storage = round(storage * order['quantity'])

            nomenclature = str(order["nm_id"])

            if self.self_sell_response.get(nomenclature):
                rub -= self.self_sell_response[nomenclature]["rub"]
                quantity -= self.self_sell_response[nomenclature]["quantity"]

            if self.prices.get(main_key):
                price = self.prices.get(main_key)
                if type(price) != int:
                    op = '-'
                    profit = '-'
                else:
                    op = round(rub - delivery - order_storage - price * quantity)
                    profit = round(op / quantity) if not quantity == 0 else op
            else:
                price = '-'
                op = '-'
                profit = '-'
                self.errors.append([main_key])

            table.append((order['supplier'], order['brand'], order['subject'],
                          order['nm_id'], order['article'], quantity,
                          rub, delivery, order_storage,
                          price, op, profit))

            base_stat["storage"] += order_storage
            base_stat["logistics"] += delivery

            if isinstance(profit, int):
                base_stat["op"] += op
                base_stat["averageProfit"] += profit
                base_stat["primeCost"] += price
                base_stat["count"] += 1
                stata += op

        self.__collect_top_orders(base_stat)
        print(stata)
        return table

    def __collect_top_orders(self, base_stat: dict):
        self.__drf_orders["baseStat"] = base_stat
        if self.__drf_orders["baseStat"]["count"]:
            self.__drf_orders["baseStat"]["averageProfit"] = round(
                self.__drf_orders["baseStat"]["averageProfit"] / self.__drf_orders["baseStat"]["count"]
            )
        else:
            self.__drf_orders["baseStat"]["averageProfit"] = 0

    def get_drf_orders(self):
        return self.__drf_orders
