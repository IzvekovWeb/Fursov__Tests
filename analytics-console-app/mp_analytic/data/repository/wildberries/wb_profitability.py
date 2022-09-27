from config.constants import WB_TOKEN
from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from domain.utils.functions import get_suppliers_list


class ProfitabilityReport(object):
    def __init__(self, wb_token, prices, suppliers=None, weeks=2):
        self.__wb_token = wb_token
        self.__suppliers = get_suppliers_list() if suppliers is None else get_suppliers_list(suppliers)
        self.storage_paid = 0
        self.count_sum = 0
        self.weeks = weeks
        self.response = {}
        self.prices = prices
        self.errors = []

    def execute(self):
        for supplier in self.__suppliers:
            print(f"Обрабатываем поставщика - {supplier.get('name')}")
            report = self.get_finance_reports_id(supplier['supplier-id'], supplier['name'])
            self.get_data(report, supplier['name'])
        return self.__get_table(), self.errors

    def get_finance_reports_id(self, supplier_id, supplier_name):
        report = []
        responses = PersonalAccountAPI().get_finance_reports_id(WB_TOKEN, supplier_id)
        responses = responses[0].get("data")[:self.weeks]
        print(f"Получение отчетов для поставщика - {supplier_name}")

        for response in responses:
            self.storage_paid += response.get("paidStorageSum")

            finance_report_id = response.get("id")
            finance_report = PersonalAccountAPI().get_weekly_finance_report(WB_TOKEN,
                                                                            supplier_id,
                                                                            finance_report_id)

            report.extend(finance_report[0].get("data").get("details"))
        return report

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

            if order_type == 'Продажа' and count == 1:
                self.response[nomenclature]['rub'] += retail_amount
                self.response[nomenclature]['quantity'] += 1
                self.count_sum += 1
            if order_type == 'Возврат' and count == 1:
                self.response[nomenclature]['rub'] -= retail_amount
                self.response[nomenclature]['quantity'] -= 1
                self.count_sum -= 1
            self.response[nomenclature]['delivery'] += order.get("deliveryRub")

    def __get_table(self):
        # TODO: try/except to check DivisionZero
        storage = self.storage_paid / self.count_sum
        print("Формируется таблица для выгрузки...")
        table = [
            ("Поставщик", "Бренд", "Предмет", "Номенклатура", "Артикул", "Продажи, шт.", "Продажи, руб.", "Логистика",
             "Хранение", "Себестоимость", "ОП", "Прибыль на 1шт.")]

        for order in self.response.values():
            rub = round(order['rub'])
            quantity = order['quantity']
            delivery = round(order['delivery'])
            order_storage = round(storage * order['quantity'])
            if self.prices.get(order['nm_id']):
                price = self.prices.get(order['nm_id'])
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
                self.errors.append([order['nm_id']])

            table.append((order['supplier'], order['brand'], order['subject'], order['nm_id'], order['article'],
                          quantity, rub, delivery, order_storage, price, op, profit))
        return table
