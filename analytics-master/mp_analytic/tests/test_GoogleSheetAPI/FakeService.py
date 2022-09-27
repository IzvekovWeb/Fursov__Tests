import os
from pathlib import Path

import pytest
from googleapiclient.errors import HttpError

from data.google.sheet.sheet_api import GoogleSheetAPI

TESTS_DIR = Path(os.path.abspath(__file__)).parent.parent


def HttpError_exception():

    class Resp400:
        def __init__(self):
            self.reason = 'Reason'
            self.status = 400

    class Resp429:
        def __init__(self):
            self.reason = 'Reason'
            self.status = 429

    raise HttpError(Resp400(), b'Answer')


def fake_batch_update(body=None):
    if body:
        return FakeBatch().executeBody
    return FakeBatch().execute


class FakeBatch():
    def executeBody(self):
        return {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'replies': [{}]}

    def execute(self):
        return {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'replies': [{}]}


class BatchUpdate(object):
    def execute(self):
        return {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'totalUpdatedRows': 3, 'totalUpdatedColumns': 1,'totalUpdatedCells': 3, 'totalUpdatedSheets': 1, 'responses': [{'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'updatedRange': 'sheet_title!A1:A3','updatedRows': 3, 'updatedColumns': 1, 'updatedCells': 3}]}


class GetAll(object):
    def execute(self):
        return {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'properties': {'title': 'Tests', 'locale': 'ru_RU', 'autoRecalc': 'ON_CHANGE', 'timeZone': 'Europe/Moscow', 'defaultFormat': {'backgroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'padding': {'top': 2, 'right': 3, 'bottom': 2, 'left': 3}, 'verticalAlignment': 'BOTTOM', 'wrapStrategy': 'OVERFLOW_CELL', 'textFormat': {'foregroundColor': {}, 'fontFamily': 'arial,sans,sans-serif', 'fontSize': 10, 'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'foregroundColorStyle': {'rgbColor': {}}}, 'backgroundColorStyle': {'rgbColor': {'red': 1, 'green': 1, 'blue': 1}}}, 'spreadsheetTheme': {'primaryFontFamily': 'Arial', 'themeColors': [{'colorType': 'TEXT', 'color': {'rgbColor': {}}}, {'colorType': 'BACKGROUND', 'color': {'rgbColor': {'red': 1, 'green': 1, 'blue': 1}}}, {'colorType': 'ACCENT1', 'color': {'rgbColor': {'red': 0.25882354, 'green': 0.52156866, 'blue': 0.95686275}}}, {'colorType': 'ACCENT2', 'color': {'rgbColor': {'red': 0.91764706, 'green': 0.2627451, 'blue': 0.20784314}}}, {'colorType': 'ACCENT3', 'color': {'rgbColor': {'red': 0.9843137, 'green': 0.7372549, 'blue': 0.015686275}}}, {'colorType': 'ACCENT4', 'color': {'rgbColor': {'red': 0.20392157, 'green': 0.65882355, 'blue': 0.3254902}}}, {'colorType': 'ACCENT5', 'color': {'rgbColor': {'red': 1, 'green': 0.42745098, 'blue': 0.003921569}}}, {'colorType': 'ACCENT6', 'color': {'rgbColor': {'red': 0.27450982, 'green': 0.7411765, 'blue': 0.7764706}}}, {'colorType': 'LINK', 'color': {'rgbColor': {'red': 0.06666667, 'green': 0.33333334, 'blue': 0.8}}}]}}, 'sheets': [{'properties': {'sheetId': 0, 'title': 'Лист1', 'index': 0, 'sheetType': 'GRID', 'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}, {'properties': {'sheetId': 195541656, 'title': 'Лист2', 'index': 1, 'sheetType': 'GRID', 'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}, {'properties': {'sheetId': 1427492153, 'title': 'Лист3', 'index': 2, 'sheetType': 'GRID', 'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}, {'properties': {'sheetId': 1144711631, 'title': 'sheet_title', 'index': 3, 'sheetType': 'GRID', 'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}], 'spreadsheetUrl': 'https://docs.google.com/spreadsheets/d/12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo/edit'}


class GetBySheetName(object):
    def execute(self):
        return {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'properties': {'title': 'Tests', 'locale': 'ru_RU', 'autoRecalc': 'ON_CHANGE', 'timeZone': 'Europe/Moscow', 'defaultFormat': {'backgroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'padding': {'top': 2, 'right': 3, 'bottom': 2, 'left': 3}, 'verticalAlignment': 'BOTTOM', 'wrapStrategy': 'OVERFLOW_CELL', 'textFormat': {'foregroundColor': {}, 'fontFamily': 'arial,sans,sans-serif', 'fontSize': 10, 'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'foregroundColorStyle': {'rgbColor': {}}}, 'backgroundColorStyle': {'rgbColor': {'red': 1, 'green': 1, 'blue': 1}}}, 'spreadsheetTheme': {'primaryFontFamily': 'Arial', 'themeColors': [{'colorType': 'TEXT', 'color': {'rgbColor': {}}}, {'colorType': 'BACKGROUND', 'color': {'rgbColor': {'red': 1, 'green': 1, 'blue': 1}}}, {'colorType': 'ACCENT1', 'color': {'rgbColor': {'red': 0.25882354, 'green': 0.52156866, 'blue': 0.95686275}}}, {'colorType': 'ACCENT2', 'color': {'rgbColor': {'red': 0.91764706, 'green': 0.2627451, 'blue': 0.20784314}}}, {'colorType': 'ACCENT3', 'color': {'rgbColor': {'red': 0.9843137, 'green': 0.7372549, 'blue': 0.015686275}}}, {'colorType': 'ACCENT4', 'color': {'rgbColor': {'red': 0.20392157, 'green': 0.65882355, 'blue': 0.3254902}}}, {'colorType': 'ACCENT5', 'color': {'rgbColor': {'red': 1, 'green': 0.42745098, 'blue': 0.003921569}}}, {'colorType': 'ACCENT6', 'color': {'rgbColor': {'red': 0.27450982, 'green': 0.7411765, 'blue': 0.7764706}}}, {'colorType': 'LINK', 'color': {'rgbColor': {'red': 0.06666667, 'green': 0.33333334, 'blue': 0.8}}}]}}, 'sheets': [{'properties': {'sheetId': 688346002, 'title': 'sheet_title', 'index': 3, 'sheetType': 'GRID', 'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}], 'spreadsheetUrl': 'https://docs.google.com/spreadsheets/d/12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo/edit'}


class GetBySheetNameException(object):
    def execute(self):
        raise HttpError_exception()

    @staticmethod
    def spreadsheets(sel=None):
        raise HttpError_exception()


class FakeService(object):
    def __init__(self):
        self.service = FakeGoogle()


class Create(object):
    def __init__(self, body):
        self.body = body

    def execute(self):
        return {'spreadsheetId': '1gvFpgZnWE79mX5C2GtQ1hEUIukmJjRY9T7jko9W9EOE', 'properties': {'title': 'New', 'locale': 'ru_RU', 'autoRecalc': 'ON_CHANGE', 'timeZone': 'Etc/GMT', 'defaultFormat': {'backgroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'padding': {'top': 2, 'right': 3, 'bottom': 2, 'left': 3}, 'verticalAlignment': 'BOTTOM', 'wrapStrategy': 'OVERFLOW_CELL', 'textFormat': {'foregroundColor': {}, 'fontFamily': 'arial,sans,sans-serif', 'fontSize': 10, 'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'foregroundColorStyle': {'rgbColor': {}}}, 'backgroundColorStyle': {'rgbColor': {'red': 1, 'green': 1, 'blue': 1}}}, 'spreadsheetTheme': {'primaryFontFamily': 'Arial', 'themeColors': [{'colorType': 'TEXT', 'color': {'rgbColor': {}}}, {'colorType': 'BACKGROUND', 'color': {'rgbColor': {'red': 1, 'green': 1, 'blue': 1}}}, {'colorType': 'ACCENT1', 'color': {'rgbColor': {'red': 0.25882354, 'green': 0.52156866, 'blue': 0.95686275}}}, {'colorType': 'ACCENT2', 'color': {'rgbColor': {'red': 0.91764706, 'green': 0.2627451, 'blue': 0.20784314}}}, {'colorType': 'ACCENT3', 'color': {'rgbColor': {'red': 0.9843137, 'green': 0.7372549, 'blue': 0.015686275}}}, {'colorType': 'ACCENT4', 'color': {'rgbColor': {'red': 0.20392157, 'green': 0.65882355, 'blue': 0.3254902}}}, {'colorType': 'ACCENT5', 'color': {'rgbColor': {'red': 1, 'green': 0.42745098, 'blue': 0.003921569}}}, {'colorType': 'ACCENT6', 'color': {'rgbColor': {'red': 0.27450982, 'green': 0.7411765, 'blue': 0.7764706}}}, {'colorType': 'LINK', 'color': {'rgbColor': {'red': 0.06666667, 'green': 0.33333334, 'blue': 0.8}}}]}}, 'sheets': [{'properties': {'sheetId': 741948705, 'title': 'Title', 'index': 0, 'sheetType': 'GRID', 'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}], 'spreadsheetUrl': 'https://docs.google.com/spreadsheets/d/1gvFpgZnWE79mX5C2GtQ1hEUIukmJjRY9T7jko9W9EOE/edit'}


class Clear(object):
    def __init__(self, range=None):
        self.range = range

    def execute(self):
        if self.range:
            if 'Empty title' in self.range:
                return {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'clearedRange': 'Empty title!A1:C2'}
        return {'spreadsheetId': '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo', 'clearedRange': 'sheet_title!A1:C2'}


class GetColumns():
    def execute(self):
        return {'range': 'sheet_title!A1:C5', 'majorDimension': 'COLUMNS', 'values': [['1'], ['2', '3', '5'], ['4']]}


class GetRows():
    def execute(self):
        return {'range': 'sheet_title!A1:C5', 'majorDimension': 'ROWS', 'values': [['1', '2', '4'], ['', '3'], ['', '5']]}


class GetAllValues():
    def __init__(self, range):
        self.range = range

    def execute(self):
        if self.range == 'Title':
            return {'range': 'Title!A1:Z1000', 'majorDimension': 'ROWS', 'values': [['11', '12'], ['21', '22']]}
        return {'range': 'Title!A1:Z1000', 'majorDimension': 'ROWS', 'values': []}


class Values(object):
    def __init__(self, range=None):
        self.range = range

    def get(self, spreadsheetId, ranges=None, range=None, includeGridData=None, majorDimension=None):
        if ranges:
            return GetBySheetName()
        if majorDimension == 'COLUMNS':
            return GetColumns()
        elif majorDimension == 'ROWS':
            return GetRows()
        return GetAllValues(range)

    def clear(self, spreadsheetId=None, range=None):
        return Clear(self.range)

    def batchUpdate(self, spreadsheetId, body):
        return BatchUpdate()


class FakeGoogle(object):

    def spreadsheets(self):
        return self

    def batchUpdate(self, spreadsheetId, body):
        return BatchUpdate()

    def get(self, spreadsheetId, ranges=None, range=None, includeGridData=None, majorDimension=None):
        if ranges:
            return GetBySheetName()
        if majorDimension == 'COLUMNS':
            return GetColumns()
        elif majorDimension == 'ROWS':
            return GetRows()
        return GetAll()

    def raiseException(self):
        raise Exception('Exception')

    def create(self, body=None):
        return Create(body)

    def values(self):
        return Values()

    def clear(self, spreadsheetId, range):
        return Clear(range)


@pytest.fixture(scope="package")
def GSA():
    sheet_title = 'Title'
    spreadsheet_id = '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo'
    sheet_id = '94459280'
    spreadsheet_title = 'Title'
    path = os.path.join(r"C:\Users\sasiz\Desktop\Работа\Fursov\analytics-master\mp_analytic\config\credits.json")
    # path = os.path.join(r"C:\Users\sasiz\Desktop\test_dir\tests\test_GoogleSheetAPI\credentials.json")
    # creds_ = os.path.join(TESTS_DIR, 'test_GoogleSheetAPI', 'credentials.json')
    creds_ = path
    GSA = GoogleSheetAPI(
        sheet_title,
        spreadsheet_id,
        sheet_id,
        spreadsheet_title,
        creds_
    )
    return GSA

# new  12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo
# old  12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo


def GSA2(sheet_title, spreadsheet_title, spreadsheet_id):
    sheet_title = 'Title'
    spreadsheet_id = '12zzJdPU5IHvYFOIevTLAP7aj1caPEfV0MpbVFUIUzSo'
    sheet_id = '94459280'
    spreadsheet_title = 'Title'
    path = os.path.join(r"C:\Users\sasiz\Desktop\Работа\Fursov\analytics-master\mp_analytic\config\credits.json")
    # creds_ = os.path.join(TESTS_DIR, 'test_GoogleSheetAPI', 'credentials.json')
    creds_ = path
    GSA = GoogleSheetAPI(
        sheet_title,
        spreadsheet_id,
        sheet_id,
        spreadsheet_title,
        creds_
    )
    return GSA
