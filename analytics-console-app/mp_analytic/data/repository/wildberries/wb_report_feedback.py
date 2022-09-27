from config.constants import WB_TOKEN
from config.suppliers import SUPPLIERS
from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.utils.functions import form_date_feedbacks, compare_dates


def get_article(article_color: str) -> str:
    return article_color.split('/')[0]


class FeedbackReport:
    def __init__(self):
        self.response = {}

    def execute(self):
        for supplier in SUPPLIERS.values():
            supplier_name = supplier.get("name")
            supplier_id = supplier.get("supplier-id")
            self.get_nomenclatures(supplier_name, supplier_id)
            self.get_feedbacks(supplier_name, supplier_id)

        return self.create_table()

    def get_feedbacks(self, supplier_name, supplier_id):
        feedback_list = PersonalAccountAPI().get_feedbacks(WB_TOKEN, supplier_id)
        feedback_article_color_list = []

        for feedback in feedback_list:

            article_color = feedback["productDetails"]["supplierArticle"]
            article = get_article(article_color)
            rate = feedback["productValuation"]
            date = form_date_feedbacks(feedback["createdDate"])

            feedback_text = feedback["text"]
            if rate == 5:
                bad_rate = "Нет"
            else:
                bad_rate = "Да"

            if article not in self.response[supplier_name].keys():
                self.response[supplier_name][article] = {
                    "nmID": {feedback["productDetails"]["nmId"]: article_color},
                    "subject": ""
                }
            else:
                if "date" in self.response[supplier_name][article].keys():
                    if compare_dates(date, self.response[supplier_name][article]["date"]):
                        feedback_article_color_list.remove(article)

            if article not in feedback_article_color_list:
                self.response[supplier_name][article]["badRate"] = bad_rate
                self.response[supplier_name][article]["rate"] = rate
                self.response[supplier_name][article]["date"] = date
                self.response[supplier_name][article]["text"] = feedback_text
                self.response[supplier_name][article]["summaryRate"] = rate
                self.response[supplier_name][article]["rateAmount"] = 1

                feedback_article_color_list.append(article)
            else:
                self.response[supplier_name][article]["summaryRate"] += rate
                self.response[supplier_name][article]["rateAmount"] += 1

    def get_nomenclatures(self, supplier_name, supplier_id):
        nomenclature_list = PersonalAccountAPI().get_nomenclatures(supplier_id)
        for nomenclature in nomenclature_list:
            self.get_unique_nomenclature_list(nomenclature, supplier_name)

    def get_unique_nomenclature_list(self, nomenclature, supplier_name):
        article_color = nomenclature["sa"]
        article = get_article(article_color)
        nm = nomenclature["nmID"]
        subject = nomenclature["subjectName"]

        if supplier_name not in self.response.keys():
            self.response[supplier_name] = {
                article: {
                    "nmID": {nm: article_color},
                    "subject": subject
                }}
        elif article not in self.response[supplier_name].keys():
            self.response[supplier_name][article] = {
                "nmID": {nm: article_color},
                "subject": subject
            }
        elif article in self.response[supplier_name].keys():
            if nm not in self.response[supplier_name][article]["nmID"]:
                self.response[supplier_name][article]["nmID"][nm] = article_color

    def create_table(self):
        table = [('Организация', 'Номенклатура', 'Артикул поставщика', 'Предмет',
                  'Плохой отзыв', 'Средний рейтинг', 'Последняя оценка', 'Дата',
                  'Отзыв'), ]
        for supplier_name, article_colors in self.response.items():
            for article, values in article_colors.items():
                nomenclatures = values["nmID"]
                subject = values["subject"]

                try:

                    bad_rate = values["badRate"]
                    rate = values["rate"]
                    date = values["date"]
                    feedback_text = values["text"]
                    average_rate = round(values["summaryRate"] / values["rateAmount"], 2)
                    for nomenclature, article_color in nomenclatures.items():
                        table.append((supplier_name, nomenclature, article_color, subject,
                                      bad_rate, average_rate, rate, date, feedback_text))

                except KeyError:
                    for nomenclature, article_color in nomenclatures.items():
                        table.append((supplier_name, nomenclature, article_color, subject,
                                      "-", "-", "-", "-", "-"))
        return table


if __name__ == '__main__':
    FeedbackReport().execute()
