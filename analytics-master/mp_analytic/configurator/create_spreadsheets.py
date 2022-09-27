from data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets import initialize_spreadsheets
from configurator.models import *


def create_spreadsheets(user_id, tariff_id):
    user = User.objects.filter(pk=user_id)
    user = user.first()
    tariff = Tariff.objects.filter(pk=tariff_id)
    tariff = tariff.first()
    user.tariff = tariff
    user.save()

    spreadsheets = initialize_spreadsheets(user.tariff.pk)
    try:
        for spreadsheet in spreadsheets.values():

            spreadsheet_id = spreadsheet.get("id")
            spreadsheet_title = spreadsheet.get("title")

            spreadsheet_object = Spreadsheet(
                spreadsheet_id=spreadsheet_id,
                spreadsheet_title=spreadsheet_title,
                user=user
            )
            spreadsheet_object.save()

            sheets = spreadsheet.get("sheets")
            for sheet in sheets.values():
                sheet_name = sheet["title"]
                sheet_id = sheet["id"]

                sheet_title_obj = Sheet.objects.filter(google_title=sheet_name)
                sheet_title_obj = sheet_title_obj.first()

                UserSheet.objects.create(
                    sheet_id=sheet_id,
                    sheet_title_id=sheet_title_obj.pk,
                    spreadsheet_id=spreadsheet_object.pk
                )
    except Exception as error:
        print(f"---------------------- {error}")
        return False
    return True
