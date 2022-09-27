from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.marketplaces.wildberries.wb_supplier_stat import SupplierStatAPI


def get_article(article_color: str) -> str:
    if article_color.find("/") > 0:
        return article_color.split('/')[0]
    return article_color


def get_article_color_size(article_color: str, size) -> str:
    return article_color + '/' + size


class SellPercentReport(object):
    def __init__(self, weeks=2, suppliers=None, self_sell_response=None):
        self.__suppliers = suppliers
        self.weeks = weeks
        self.response_by_article_color = {}
        self.response_by_subject = {}
        self.response_by_article = {}
        self.response_by_article_color_size = {}

        if self_sell_response is None:
            self_sell_response = {}
        self.self_sell_response = self_sell_response

    def execute(self):
        self.get_finance_reports_id()
        return self.create_table()

    def get_finance_reports_id(self):

        for supplier in self.__suppliers:
            print(f"\rОбрабатываем - {supplier.get('name')}")
            responses = PersonalAccountAPI().get_finance_reports_id(supplier.get('wb_token'),
                                                                    supplier.get("supplier-id"))
            if isinstance(responses, list):
                responses = responses[0].get("data")[:self.weeks]

                for response in responses:
                    finance_report_id = response.get("id")
                    try:
                        finance_report = PersonalAccountAPI().get_weekly_finance_report(supplier.get('wb_token'),
                                                                                        supplier["supplier-id"],
                                                                                        finance_report_id)
                        if not isinstance(finance_report, list):
                            finance_report = []
                        self.get_data_from_finance_report(finance_report)
                    except ConnectionError:
                        self.get_data_from_api([response["dateFrom"], response["dateTo"]], supplier)
                        print("Working API...")

    def get_data_from_api(self, dates, supplier):
        finance_report = SupplierStatAPI.report_detail_by_period(supplier, dates)
        for order in finance_report:
            subject = order.get("subject_name") or ""
            article_color = order.get("sa_name") or ""
            size = order.get("ts_name") or ""
            nomenclature = order.get("nomenclatureId") or ""

            order_type = order.get("doc_type_name")
            count = order.get("quantity")
            return_amount = order.get("return_amount")

            article = get_article(article_color)
            article_color_size = get_article_color_size(article_color, size)

            args = [article_color, subject, article, article_color_size, nomenclature]

            self.prepare_data(order_type, count, return_amount, *args)

    def get_data_from_finance_report(self, finance_report: list):
        for order in finance_report:
            subject = order.get("subject").get("name")
            article_color = order.get("articleSupplier")
            size = order.get("size").get("name")
            order_type = order.get("type")
            count = order.get("quantity")
            return_amount = order.get("returnAmount")
            nomenclature = order.get("nomenclatureId")

            article = get_article(article_color)
            article_color_size = get_article_color_size(article_color, size)

            args = [article_color, subject, article, article_color_size, nomenclature]

            self.prepare_data(order_type, count, return_amount, *args)

    def prepare_data(self, order_type: str, count, return_amount: int, *args: list):
        if order_type == "Продажа" and count:
            pay = 1
        else:
            pay = 0

        if order_type == "Возврат" and count:
            return_item = 1
        else:
            return_item = 0

        sell = pay - return_item
        orders = pay + return_amount

        if orders:
            percent = sell / orders
            if percent < 0:
                percent = 0
        else:
            percent = 0

        article_color = args[0]
        subject = args[1]
        article = args[2]
        article_color_size = args[3]
        nomenclature = str(args[4])

        self.percent(self.response_by_article_color, article_color, orders,
                     pay, return_amount, return_item, sell, percent, nomenclature)

        self.percent(self.response_by_subject, subject, orders, pay,
                     return_amount, return_item, sell, percent, nomenclature)

        self.percent(self.response_by_article, article, orders, pay,
                     return_amount, return_item, sell, percent, nomenclature)

        self.percent(self.response_by_article_color_size, article_color_size,
                     orders, pay, return_amount, return_item, sell, percent, nomenclature)

    def percent(self, main_dict, main_key, orders, pay,
                return_amount, return_item, sell, percent, nomenclature):

        if self.self_sell_response.get(nomenclature):
            if self.self_sell_response[nomenclature].get("quantity"):
                quantity = self.self_sell_response[nomenclature].get("quantity")
                orders -= quantity
                sell -= quantity
                self.self_sell_response.pop(nomenclature)

        if main_key not in main_dict.keys():

            main_dict[main_key] = {
                "orders": orders,
                "cancel": return_amount,
                "pay": pay,
                "return_item": return_item,
                "sell": sell,
                "percent": percent
            }
        else:
            main_dict[main_key]["orders"] += orders
            main_dict[main_key]["cancel"] += return_amount
            main_dict[main_key]["pay"] += pay
            main_dict[main_key]["return_item"] += return_item
            main_dict[main_key]["sell"] += sell

            if main_dict[main_key]["orders"]:
                _percent = main_dict[main_key]["sell"] / main_dict[main_key]["orders"]
                _percent = round(_percent * 100, 1)
                main_dict[main_key]["percent"] = _percent

    def create_table(self):
        article_color_header = "Артикул/Цвет"
        subject_header = "Предмет"
        article_header = "Артикул"
        article_color_size_header = "Артикул/Цвет/Размер"
        main_header = ("Заказы", "Отказы", "Оплаты", "Возвраты", "Продажи", "% Выкупа")

        tables = [
            [(article_color_header, *main_header), ],
            [(subject_header, *main_header), ],
            [(article_header, *main_header), ],
            [(article_color_size_header, *main_header), ],
        ]
        self.collect_data(self.response_by_article_color, tables[0])
        self.collect_data(self.response_by_subject, tables[1])
        self.collect_data(self.response_by_article, tables[2])
        self.collect_data(self.response_by_article_color_size, tables[3])
        return tables

    def collect_data(self, response: dict, table: list):
        for key, values in response.items():
            row = (values["orders"],
                   values["cancel"],
                   values["pay"],
                   values["return_item"],
                   values["sell"],
                   values["percent"])
            table.append((key, *row))
