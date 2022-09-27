import time

from data.google.sheet.sheet_api import GoogleSheetAPI


def insert_header(table: GoogleSheetAPI, headers: list):
    values = [(
        *headers,
    )]
    table.insert(values=values)
    time.sleep(5)
    end_column = len(values[0])
    table.borders(start_column=0,
                  end_column=end_column,
                  end_row=500,
                  top=False,
                  style='SOLID_THICK')
    time.sleep(5)
    table.borders(start_column=0,
                  end_column=end_column,
                  start_row=0,
                  end_row=1,
                  top=False,
                  left=False,
                  style='SOLID_THICK')
