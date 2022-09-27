import time

import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError

from config.color_constants import *
from config.format_type_constants import *
from data.google.update_cells.update_borders import update_borders
from config.constants import APIS, GOOGLE_SHEETS_FILE
from data.google.get_body_methods.get_body import *
from data.google.get_range_methods.get_range import *


class GoogleSheetAPI(object):
    def __init__(self,
                 sheet_title,
                 spreadsheet_id,
                 sheet_id='0',
                 spreadsheet_title='Wildberries',
                 creds=GOOGLE_SHEETS_FILE):

        credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, APIS)
        self.http_auth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.http_auth)  # Service account
        self.spreadsheet_id = spreadsheet_id  # Spreadsheet ID
        self.spreadsheet_title = spreadsheet_title  # Title of SpreadSheet
        self.sheet_title = sheet_title  # Title of sheet
        self.sheet_id = sheet_id  # Sheet ID

    def create_sheet(self) -> str:
        """
        Creating new sheet on existing spreadsheet\n
        :return: Sheet's ID
        """

        if self.spreadsheet_id:
            self.add_sheet()
        else:
            spreadsheet = self.spreadsheet_create()
            self.spreadsheet_id = spreadsheet['spreadsheetId']
            self.access_for_new_table()

        self.sheet_id = self.get_sheet_id(self.sheet_title)
        return self.sheet_id

    def spreadsheet_create(self):
        body = get_body_create_spreadsheet(self.spreadsheet_title, self.sheet_title)
        try:
            execute_function = self.service.spreadsheets().create(body=body).execute
        except Exception as err:
            print(err)
            return False
        return self.call_function(execute_function)

    def access_for_new_table(self):
        drive_service = apiclient.discovery.build('drive', 'v3', http=self.http_auth)
        drive_service.permissions().create(fileId=self.spreadsheet_id,
                                           body={'type': 'anyone', 'role': 'writer'},
                                           fields='id').execute()

    def add_sheet(self):
        if self.if_exists():
            return False
        body = get_body_add_sheet(self.sheet_title)

        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    def get_sheet_url(self) -> str:
        """
        Генерация ссылки на таблицу
        :return: ссылка на таблицу
        """
        return 'https://docs.google.com/spreadsheets/d/' + self.spreadsheet_id + '/edit#gid=' + str(self.sheet_id)

    def get_sheet_id(self, sheet_name=None):
        if not sheet_name:
            sheet_name = self.sheet_title

        resp = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id, ranges=sheet_name,
                                               includeGridData=False).execute()
        sheet_id = resp.get("sheets")[0].get("properties").get("sheetId")
        return sheet_id

    def if_exists(self, sheet_name=None) -> bool:
        """
        Check existence of Sheet\n
        :param sheet_name: The name of sheet of GoogleSheets
        :return: True if sheet exists, False if not
        """

        if not sheet_name:
            sheet_name = self.sheet_title

        try:
            execute_function = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute
        except Exception as err:
            print(err)
            return False
        sheets = self.call_function(execute_function)
        for sheet in sheets['sheets']:
            if sheet_name == sheet['properties']['title']:
                return True
        return False

    def clear(self, start_column=None, end_column=None, sheet_name=None) -> bool:
        """
        Cleaning sheet by range\n
        :param start_column: Start column of the cleaning range
        :param end_column: End column of the cleaning range
        :param sheet_name: Sheet's title
        :return:
        """
        if not sheet_name:
            sheet_name = self.sheet_title

        _range = get_range(start_column, end_column, sheet_name)

        try:
            execute_function = self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id,
                                                                          range=_range).execute
        except Exception as err:
            print(err)
            return False
        return self.call_function(execute_function)

    def get_column(self, column_begin, column_end=None, sheet_name=None) -> list:
        """
        Get Columns from sheet\n
        :param sheet_name: The name of sheet of GoogleSheets
        :param column_begin: The start Column
        :param column_end: The end Column
        :return: List of values
        """

        if not sheet_name:
            sheet_name = self.sheet_title
        _range = get_range_column_row(column_begin, column_end, sheet_name)

        try:
            execute_function = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                                                        range=_range,
                                                                        majorDimension='COLUMNS').execute
        except Exception as err:
            print(err)
            return []
        values = self.call_function(execute_function)
        values = values.get('values', [])
        if not values:
            print('No data found.')
            return []
        else:
            return values

    def get_row(self, row_begin, row_end=None, sheet_name=None) -> list:
        """
        Get Rows from sheet\n
        :param sheet_name: The name of sheet of GoogleSheets
        :param row_begin: The first Row
        :param row_end: The second Row
        :return: List of values
        """

        if not sheet_name:
            sheet_name = self.sheet_title
        _range = get_range_column_row(row_begin, row_end, sheet_name)

        try:
            execute_function = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                                                        range=_range,
                                                                        majorDimension='ROWS').execute
        except Exception as err:
            print(err)
            return []
        values = self.call_function(execute_function)
        values = values.get('values', [])
        if not values:
            print('No data found.')
            return []
        else:
            return values

    def insert(self, values, start_column=None, end_column=None, sheet_name=None) -> bool:
        """
        Insert data in defined cells\n
        :param values: values to insert into table
        :param start_column: Start column of the cleaning range
        :param end_column: End column of the cleaning range
        :param sheet_name: Title of sheet
        :return: True if values inserted, False if not
        """

        if not sheet_name:
            sheet_name = self.sheet_title

        _range = get_range(start_column, end_column, sheet_name)
        body = get_body_insert(_range, values)

        try:
            execute_function = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                                                body=body).execute
        except Exception as err:
            print(err)
            return False
        total_update_cells = self.call_function(execute_function)
        total_update_cells = total_update_cells.get('totalUpdatedCells')
        if not total_update_cells:
            print('----- No data inserted')
            return False
        else:
            return True

    def get(self, sheet_name=None):
        """
        Get Data from sheet\n
        :param sheet_name: The name of sheet of GoogleSheets
        :return: List of values
        """
        if not sheet_name:
            sheet_name = self.sheet_title

        try:
            execute_function = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                                                        range=sheet_name).execute
        except Exception as err:
            print(err)
            return []
        values = self.call_function(execute_function)
        values = values.get('values', [])
        if not values:
            print('No data found.')
            return []
        else:
            return values

    def insert_feedbacks(self, values, feedback_list, sheet_name=None):
        if not sheet_name:
            sheet_name = self.sheet_title
        body = {
            "range": sheet_name,
            "majorDimension": "ROWS",
            "values": values
        }
        try:
            self.service.spreadsheets().values().append(spreadsheetId=self.spreadsheet_id,
                                                        range=sheet_name,
                                                        valueInputOption='USER_ENTERED',
                                                        insertDataOption='INSERT_ROWS',
                                                        body=body).execute()

            body = {"requests": []}
            for row in range(len(feedback_list)):

                if feedback_list[row][7] < 5:
                    while True:
                        try:
                            body['requests'].append([
                                {
                                    "repeatCell": {
                                        "range": {
                                            "sheetId": self.sheet_id,
                                            "startRowIndex": row + 1,
                                            "endRowIndex": row + 2,
                                            "startColumnIndex": 7,
                                            "endColumnIndex": 10,
                                        },
                                        "cell": {
                                            "userEnteredFormat": {
                                                "textFormat": {
                                                    "foregroundColor": {
                                                        "red": 25,
                                                        "green": 0,
                                                        "blue": 0},
                                                    "fontFamily": "Arial",
                                                    "bold": False
                                                }
                                            },
                                        },
                                        "fields": "userEnteredFormat(textFormat)"
                                    }
                                }
                            ])

                            break
                        except HttpError as err:
                            print('-----', err)
                            return []
            self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
            print("Готово")
        except HttpError as err:
            print('-----', err)
            return []

    def colorize_row(self, body=None):
        if not body:
            body = {"requests": []}
            get_body_colorize(body=body,
                              _range=get_range_colorize(sheet_id=self.sheet_id),
                              _color=WHITE)
        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    def conditional_color_format(self, start_row, end_row):
        body = get_body_conditional_color_format(self.sheet_id,
                                                 start_row,
                                                 end_row,
                                                 RED_DEEP,
                                                 YELLOW,
                                                 GREEN_DEEP)

        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    def number_format(self, start_row, end_row, start_column, end_column, sheet_id=None):
        if sheet_id:
            self.sheet_id = sheet_id
        body = get_body_format(self.sheet_id,
                               start_row,
                               end_row,
                               start_column,
                               end_column,
                               NUMBER_FORMAT_TYPE_NUMBER,
                               NUMBER_FORMAT_PATTERN_NUMBER)

        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    def percent_format(self, start_row, end_row, start_column, end_column):
        body = get_body_format(self.sheet_id,
                               start_row,
                               end_row,
                               start_column,
                               end_column,
                               NUMBER_FORMAT_TYPE_PERCENT,
                               NUMBER_FORMAT_PATTERN_PERCENT)

        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    def clear_cond(self):
        body = get_body_clear_conditions(self.sheet_id)
        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    def borders(self, start_row=None, end_row=None,
                start_column=None, end_column=None,
                left=True, right=True, bottom=True, top=True,
                width=1, style='SOLID', color=BLACK, clear=0):

        body = update_borders(self.sheet_id, start_row, end_row,
                              start_column, end_column,
                              left, right, bottom, top,
                              width, style, color, clear)

        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    def colorize_dynamic(self, body):
        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    def batch_update(self, body):
        try:
            return self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                           body=body).execute
        except Exception as err:
            print(err)
            return False

    def call_function(self, execute_function):
        while True:
            try:
                return execute_function()
            except HttpError as err:
                print('-----', err)
                if err.status_code == 429:  # Limit 'Write requests per minute per user'
                    time.sleep(5)
                    continue
                print('-----', err)
                return False
