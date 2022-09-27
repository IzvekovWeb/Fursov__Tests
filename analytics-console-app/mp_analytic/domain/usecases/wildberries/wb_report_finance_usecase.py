from mp_analytic.config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from mp_analytic.data.google.sheet.sheet_api import GoogleSheetAPI
from mp_analytic.data.repository.wildberries.wb_report_finance import FinanceReport


class FinanceReportUseCase:
    """
    Фин-отчет
    """

    def execute(self) -> str:
        sheet_title = SHEETS.get('region_remains').get('title')
        sheet_id = SHEETS.get('region_remains').get('id')

        response, storage_paid = FinanceReport(2).execute()

        table = GoogleSheetAPI('Фин-отчет', SPREADSHEET_ID_SECOND, 2000929022)

        table.clear()
        table.insert(response)

        table.insert([["Стоимость хранения"], [storage_paid]], "N")

        return table.get_sheet_url()


if __name__ == '__main__':
    FinanceReportUseCase().execute()
