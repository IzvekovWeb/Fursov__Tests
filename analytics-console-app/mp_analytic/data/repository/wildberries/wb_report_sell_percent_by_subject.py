from config.constants import WB_TOKEN
from config.suppliers import SUPPLIERS
from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI


class SellPercentBySubjectReport(object):
    def __init__(self, weeks=8):
        self.weeks = weeks
        self.response_by_subject = {}

    def execute(self):
        self.get_finance_reports_id()
        return self.create_table()

    def get_finance_reports_id(self):

        for supplier in SUPPLIERS.values():
            print(f"\rОбрабатываем - {supplier.get('name')}")
            responses = PersonalAccountAPI().get_finance_reports_id(WB_TOKEN, supplier["supplier-id"])
            responses = responses[0].get("data")[:self.weeks]

            for response in responses:
                finance_report_id = response.get("id")
                finance_report = PersonalAccountAPI().get_weekly_finance_report(WB_TOKEN,
                                                                                supplier["supplier-id"],
                                                                                finance_report_id)

                finance_report = finance_report[0].get("data").get("details")
                self.get_data_from_finance_report(finance_report)

    def get_data_from_finance_report(self, finance_report):
        for order in finance_report:
            subject = order.get("subject").get("name")
            order_type = order.get("type")
            count = order.get("quantity")
            return_amount = order.get("returnAmount")

            self.prepare_data(order_type, count, return_amount, subject)

    def prepare_data(self, order_type, count, return_amount, article_color):
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

        self.percent(self.response_by_subject, article_color, orders,
                     pay, return_amount, return_item, sell, percent)

    def percent(self, main_dict, main_key, orders, pay, return_amount, return_item, sell, percent):
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
        subject_header = "Предмет"
        main_header = ("Заказы", "Отказы", "Оплаты", "Возвраты", "Продажи", "% Выкупа")

        tables = [
            (subject_header, *main_header),
        ]
        self.collect_data(self.response_by_subject, tables)
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
