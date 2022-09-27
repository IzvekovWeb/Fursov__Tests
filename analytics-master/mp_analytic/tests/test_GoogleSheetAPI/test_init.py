import os

from pathlib import Path
from FakeService import GSA
from data.google.sheet.sheet_api import GoogleSheetAPI

TESTS_DIR = Path(os.path.abspath(__file__)).parent.parent


def test_init():
    sheet_title = 12345678
    spreadsheet_id = '1tVNxI8os2lyFNbsIQsKHxHzgRTL69YDwNb9B3tJPmNc'
    sheet_id = '287693396',
    spreadsheet_title = 'Title',
    creds_ = os.path.join(TESTS_DIR, 'test_GoogleSheetAPI', 'credentials.json')

    result = GoogleSheetAPI(
        sheet_title,
        spreadsheet_id,
        sheet_id,
        spreadsheet_title,
        creds_
    )

    assert result.spreadsheet_id == spreadsheet_id
    assert result.spreadsheet_title == spreadsheet_title
    assert result.sheet_id == sheet_id
    assert result.sheet_title == sheet_title
