from data.google.sheet.sheet_api import GoogleSheetAPI


def insert_plan(spreadsheet_id, sheet_id, sheet_title, data, row_num):

    table = GoogleSheetAPI(sheet_title, spreadsheet_id, sheet_id)
    return table.insert([data], start_column=row_num, end_column=row_num)
