from mp_analytic.config.constants import WB_TOKEN
from mp_analytic.config.suppliers import SUPPLIERS
from mp_analytic.data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI


class FinanceReport(object):
    def __init__(self, weeks=8):
        self.table = [("Организация", "Номенклатура", "Предмет", "Артикул/Цвет",
                       "Размер", "Бренд", "Штрихкод", "Склад", "Тип документа",
                       "Кол-во", "Кол-во возвратов", "Цена", "Доставка")]
        self.storage_paid = 0
        self.weeks = weeks

    def execute(self):
        self.get_finance_reports_id()
        return self.table, self.storage_paid

    def get_finance_reports_id(self):

        for supplier in SUPPLIERS.values():
            responses = PersonalAccountAPI().get_finance_reports_id(WB_TOKEN, supplier["supplier-id"])
            responses = responses[0].get("data")[:self.weeks]

            for response in responses:
                self.storage_paid += response.get("paidStorageSum")

                finance_report_id = response.get("id")
                finance_report = PersonalAccountAPI().get_weekly_finance_report(WB_TOKEN,
                                                                                supplier["supplier-id"],
                                                                                finance_report_id)

                finance_report = finance_report[0].get("data").get("details")
                self.get_data_from_finance_report(finance_report, supplier.get("name"))

    def get_data_from_finance_report(self, finance_report, supplier_name):
        for order in finance_report:

            nomenclature = order.get("nomenclatureId")
            subject = order.get("subject").get("name")
            article_color = order.get("articleSupplier")
            size = order.get("size").get("name")
            brand = order.get("brand").get("name")
            barcode = order.get("barcode")
            warehouse = order.get("warehouse").get("name")
            order_type = order.get("type")
            count = order.get("quantity")
            return_amount = order.get("returnAmount")
            reward = order.get("supplierReward")
            delivery = order.get("deliveryRub")

            self.table.append((supplier_name, nomenclature, subject,
                               article_color, size, brand, barcode,
                               warehouse, order_type, count,
                               return_amount, reward, delivery))
