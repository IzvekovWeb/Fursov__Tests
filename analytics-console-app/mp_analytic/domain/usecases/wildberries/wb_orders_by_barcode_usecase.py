from config.sheets import SHEETS, SPREADSHEET_ID_SECOND
from data.google.sheet.sheet_api import GoogleSheetAPI
from data.repository.wildberries.wb_orders_by_barcode import OrdersByBarcode


class OrdersByBarcodeUseCase:
    """
    Отчет "Заказы (все)"
    """

    def execute(self, days_count: int = 7) -> str:
        response = OrdersByBarcode(days_count).execute()
        sheet_title = SHEETS.get('orders_all').get('title')
        sheet_id = SHEETS.get('orders_all').get('id')

        table = GoogleSheetAPI(sheet_title, SPREADSHEET_ID_SECOND, sheet_id)
        table.clear()
        table.insert(response)
        return table.get_sheet_url()
