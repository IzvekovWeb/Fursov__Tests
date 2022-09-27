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
    """
    GooGleSheetAPI class

    ...
    Attributes:
    -------
    sheet_title : str
        Sheet title
    spreadsheet_id : str
        Spreadsheet ID
    sheet_id: str
        Sheet ID
    spreadsheet_title: str
        Spreadsheet title
    service:
        Resource object with methods for interacting with the Google service
    creds: str
        Path to credentials json

    Methods
    -------
    create_sheet() -> str


    """

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
        """
        Creating new spreadsheet
        :return: JSON created spreadsheet
        """

        body = get_body_create_spreadsheet(self.spreadsheet_title, self.sheet_title)
        try:
            execute_function = self.service.spreadsheets().create(body=body).execute
        except Exception as err:
            print(err)
            return False
        return self.call_function(execute_function)

    def access_for_new_table(self):
        """Granted access for new table"""

        drive_service = apiclient.discovery.build('drive', 'v3', http=self.http_auth)
        drive_service.permissions().create(fileId=self.spreadsheet_id,
                                           body={'type': 'anyone', 'role': 'writer'},
                                           fields='id').execute()

    def add_sheet(self):
        """
        Create new sheet
        :return: JSON created sheet
        """

        if self.if_exists():
            return False
        body = get_body_add_sheet(self.sheet_title)

        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    def get_sheet_url(self) -> str:
        """
        Generates a link to the table
        :return: link to the table
        """
        return 'https://docs.google.com/spreadsheets/d/' + self.spreadsheet_id + '/edit#gid=' + str(self.sheet_id)

    def get_sheet_id(self, sheet_name: str | None = None):
        """
        Returns sheet ID
        :param str | None sheet_name: The name of sheet of GoogleSheets
        :return: Sheet ID
        """

        if not sheet_name:
            sheet_name = self.sheet_title

        resp = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id, ranges=sheet_name,
                                               includeGridData=False).execute()
        sheet_id = resp.get("sheets")[0].get("properties").get("sheetId")
        return sheet_id

    def if_exists(self, sheet_name: str | None = None) -> bool:
        """
        Check existence of Sheet\n
        :param str | None sheet_name: The name of sheet of GoogleSheets
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

    @check_instance
    def clear(self, start_column: int | str | None = None,
              end_column: int | str | None = None,
              sheet_name: str | None = None) -> bool:
        """
        Cleaning sheet by range\n
        :param int | str | None start_column: Start column of the cleaning range
        :param int | str | None end_column: End column of the cleaning range
        :param str | None sheet_name: Sheet's title
        :return: JSON about cleared spreadsheet
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

    @check_instance
    def get_column(self, column_begin: str | int,
                   column_end: str | int = None,
                   sheet_name: str | int = None) -> list:
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

    @check_instance
    def get_row(self, row_begin: int | str, row_end: int | str = None, sheet_name: int | str = None) -> list:
        """
        Get Rows from sheet
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

    def insert(self, values: list,
               start_column: int | str = None,
               end_column: int | str = None,
               sheet_name: int | str = None) -> bool:
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

    @check_instance
    def get(self, sheet_name: int | str = None) -> list:
        """
        Get values from sheet\n
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

    @check_instance
    def insert_feedbacks(self, values: list, feedback_list: list, sheet_name: int | str = None) -> None | list:
        """Inserts feedbacks
        :param values: List of feedbacks
        :param feedback_list:
        :param sheet_name: The name of sheet of GoogleSheets
        """
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

    @check_instance
    def colorize_row(self, body: dict = None):
        """
        Make row colorized
        :param body:
        :return: JSON
        """

        if not body:
            body = {"requests": []}
            get_body_colorize(body=body,
                              _range=get_range_colorize(sheet_id=self.sheet_id),
                              _color=WHITE)
        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    @check_instance
    def conditional_color_format(self, start_row: int | str, end_row: int | str):
        """
        Added condition for color format on rows
        :param start_row: Start row
        :param end_row: End row
        :return: JSON
        """
        body = get_body_conditional_color_format(self.sheet_id,
                                                 start_row,
                                                 end_row,
                                                 RED_DEEP,
                                                 YELLOW,
                                                 GREEN_DEEP)

        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    @check_instance
    def number_format(self, start_row: int | str, end_row: int | str,
                      start_column: int | str, end_column: int | str,
                      sheet_id: int | str = None):
        """
        Formatting cells to number format
        :param start_row:
        :param end_row:
        :param start_column:
        :param end_column:
        :param sheet_id:
        :return: JSON
        """
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

    @check_instance
    def percent_format(self, start_row: int | str, end_row: int | str, start_column: int | str, end_column: int | str):
        """
        Formatting cells to percent format
        :param start_row:
        :param end_row:
        :param start_column:
        :param end_column:
        :return: JSON
        """
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
        """Delete last color conditional"""

        body = get_body_clear_conditions(self.sheet_id)
        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    @check_instance
    def borders(self, start_row: int | str | None = None, end_row: int | str | None = None,
                start_column: int | str | None = None, end_column: int | str | None = None,
                left: bool = True, right: bool = True, bottom: bool = True, top: bool = True,
                width: int = 1, style: str = 'SOLID', color: dict = BLACK, clear: bool = False):
        """
        Stiled borders
        :param start_row:
        :param end_row:
        :param start_column:
        :param end_column:
        :param left:
        :param right:
        :param bottom:
        :param top:
        :param width:
        :param style:
        :param color:
        :param boolean clear:
        :return:
        """

        body = update_borders(self.sheet_id, start_row, end_row,
                              start_column, end_column,
                              left, right, bottom, top,
                              width, style, color, clear)

        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    @check_instance
    def colorize_dynamic(self, body: dict):
        execute_function = self.batch_update(body)
        return self.call_function(execute_function)

    def batch_update(self, body: dict):
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
