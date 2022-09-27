from application.controllers.wb_reports_drf import ReportsDRF
from data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets import initialize_spreadsheets
from .models import User, Spreadsheet, UserSheet, Sheet
from rest_framework import serializers
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {
            "write_only": True
        }}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, request):
        self.token = request['refresh']
        return request

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class UserViewSerializer(serializers.ModelSerializer):
    tariff_title = serializers.CharField(source="tariff.title")

    class Meta:
        model = User
        fields = ["username", "email", "full_name", "phone_num",
                  "date_follow", "date_expire", "tariff_id", "tariff_title"]


class SpreadsheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spreadsheet
        fields = ["user", ]

    def create(self, validated_data):
        user = validated_data.get("user")

        spreadsheets = initialize_spreadsheets(user.tariff.pk)
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
                sheet_name = sheet["title_db"]
                sheet_id = sheet["id"]

                sheet_title_obj = Sheet.objects.filter(title=sheet_name)[0]

                UserSheet.objects.create(
                    sheet_id=sheet_id,
                    sheet_title_id=sheet_title_obj.pk,
                    spreadsheet_id=spreadsheet_object.pk
                )
        return User


class SpreadsheetViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spreadsheet
        fields = ["id", "spreadsheet_title", "spreadsheet_id", ]


class SheetViewSerializer(serializers.ModelSerializer):
    spreadsheet_id = serializers.CharField(source="spreadsheet.spreadsheet_id")
    spreadsheet_title = serializers.CharField(source="spreadsheet.spreadsheet_title")

    sheet_name = serializers.CharField(source="sheet_title.title")

    class Meta:
        model = UserSheet
        fields = ["id", "update_at", "sheet_title_id", "sheet_name",
                  "sheet_id", "spreadsheet_id", "spreadsheet_title"]


class SheetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSheet
        fields = ["update_at"]

    def update(self, instance, validated_data):
        reports = ReportsDRF()
        reports.execute()

        title_dict = reports.get_title_dict()
        report = title_dict.get(instance.sheet_title.title)

        instance.update_at = report.execute()
        instance.save()

        return instance
