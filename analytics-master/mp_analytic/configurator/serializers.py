import datetime
import os

from django.utils.text import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from data.marketplaces.wildberries.wb_wild_token import encode_token
from domain.utils.wb_reports_drf import ReportsDRF
from data.google.wb_initialize_spreadsheets.wb_initialize_spreadsheets import initialize_spreadsheets
from data.marketplaces.wildberries.wb_auth import WBAuth
from .utils import *


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


class RequestConfirmCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_num"]

    def update(self, instance: User, validated_data: dict):
        phone_num = validated_data.pop("phone_num")
        instance.phone_num = phone_num
        instance.save()

        wb_auth_object = WBAuth(phone_num)
        while True:
            if wb_auth_object.check_phone_number():
                message = wb_auth_object.request_confirm_code()
                break
            raise (ValueError, TypeError)
        return instance, message


class ConfirmCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentials
        fields = []

    def update(self, instance: User, validated_data: dict):
        code = validated_data.pop("code")

        wb_auth_object = WBAuth(instance.phone_num)
        token_v3: str = wb_auth_object.post_confirm_code(code)
        if not token_v3:
            raise ValueError

        wb_token, suppliers = wb_auth_object.get_wb_token(token_v3)
        instance.token_v3 = wb_auth_object.get_wild_token()
        instance.save()

        old_instances = self.Meta.model.objects.filter(user=instance.pk)
        if old_instances:
            old_instances.delete()

        new_instance = self.Meta.model
        for supplier in suppliers:
            print(supplier.get("name"))
            x64key, access_token = wb_auth_object.get_external_keys(wb_token, supplier.get("id"))
            new_instance = self.Meta.model(
                user=instance,
                wb_token=wb_token,
                name=supplier.get("name"),
                organization=supplier.get("fullName"),
                token=access_token,
                x64key=x64key,
                supplier_id=supplier.get("id")
            )
            new_instance.save()

        return new_instance


class TokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentials
        fields = ["id", "name", "token", "x64key"]

    def update(self, instance, validated_data: dict):
        data_list: list = validated_data.get("data")
        for model in instance:
            for data in data_list:
                if model.name in data.get("name"):
                    if data.get("x64key") and data.get("token"):
                        model.x64key = data.get("x64key")
                        model.token = data.get("token")
                        model.save()
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

    date_follow = serializers.DateTimeField(read_only=True, format="%d.%m.%Y")
    date_expire = serializers.DateTimeField(read_only=True, format="%d.%m.%Y")

    class Meta:
        model = User
        fields = ["username", "email", "full_name", "phone_num",
                  "date_follow", "date_expire", "tariff"]


class SpreadsheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spreadsheet
        fields = ["id", ]

    def create(self, validated_data):
        user = User.objects.filter(pk=validated_data.get('pk'))
        user = user.first()

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
                sheet_name = sheet["title"]
                sheet_id = sheet["id"]

                sheet_title_obj = Sheet.objects.filter(google_title=sheet_name)
                sheet_title_obj = sheet_title_obj.first()

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

    slug = serializers.CharField(source="sheet_title.slug")
    has_detail = serializers.CharField(source="sheet_title.has_detail")
    secondary = serializers.CharField(source="sheet_title.secondary")
    description = serializers.CharField(source="sheet_title.description")
    sheet_name = serializers.CharField(source="sheet_title.title")
    update_at = serializers.DateTimeField(read_only=True, format="%d.%m.%Y %H:%M")

    class Meta:
        model = UserSheet
        fields = ["id", "update_at", "sheet_title_id", "sheet_name",
                  "sheet_id", "spreadsheet_id", "spreadsheet_title",
                  "has_detail", "secondary", "description", "slug"]


class SingleSheetViewSerializer(SheetViewSerializer):
    class Meta:
        model = UserSheet
        fields = ["id", "update_at", "sheet_title_id", "sheet_name",
                  "sheet_id", "spreadsheet_id", "spreadsheet_title",
                  "has_detail", "secondary", "description"]


class SheetUpdateSerializer(serializers.ModelSerializer):
    update_at = serializers.DateTimeField(read_only=True, format="%d.%m.%Y %H:%M")

    class Meta:
        model = UserSheet
        fields = ["update_at"]

    def update(self, instance, validated_data):
        if isinstance(instance, Response):
            return instance

        reports = ReportsDRF()
        reports.execute()

        kwargs = {}

        user_id = instance.spreadsheet.user.pk
        spreadsheets = Spreadsheet.objects.filter(user_id=user_id)

        for spreadsheet in spreadsheets:
            kwargs[spreadsheet.spreadsheet_title] = spreadsheet.spreadsheet_id
            sheets = UserSheet.objects.filter(spreadsheet_id=spreadsheet.pk)
            for sheet in sheets:
                kwargs[sheet.sheet_title.google_title] = sheet.sheet_id

        creds = UserCredentials.objects.filter(user=user_id)
        kwargs["suppliers"] = []
        for cred in creds:
            kwargs["suppliers"].append({
                "wb_token": cred.wb_token,
                "name": cred.name,
                "supplier-id": cred.supplier_id,
                "token": cred.token,
                "x64key": cred.x64key
            })
        kwargs["user_id"] = user_id

        title_dict = reports.get_title_dict()
        report = title_dict.get(instance.sheet_title.title)

        report = report(kwargs)
        try:
            instance.update_at = report.execute()

            if not instance.update_at:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            instance.save()
        except PermissionError:
            user = instance.spreadsheet.user
            token_v3 = user.token_v3
            if not token_v3:
                raise ValueError

            wb_auth_object = WBAuth(user.phone_num)
            # de_token = encode_token(token_v3 + os.environ.get("SECRET_TOKEN"))
            # wb_token, suppliers = wb_auth_object.get_wb_token(de_token)
            wb_token, suppliers = wb_auth_object.get_wb_token(token_v3)

            user_creds = UserCredentials.objects.filter(user=user_id)
            for user_cred in user_creds:
                user_cred.wb_token = wb_token
                user_cred.save()

            print(f"WB_TOKEN IS INVALID\n++++++++++  USER: {user} ++++++++++")
            raise PermissionError

        if instance.sheet_title.slug in SLUG:
            spreadsheet_id = instance.spreadsheet.pk
            spreadsheet = Spreadsheet.objects.get(pk=spreadsheet_id)

            user = spreadsheet.user

            dashboard_data = report.dashboard_data

            if instance.sheet_title.slug == "dynamic-art-count":
                top_orders_table(user, dashboard_data)
                top_orders_graph(user, dashboard_data)
                top_brands_table(user, dashboard_data)
                base_stat_dynamic_orders(user, dashboard_data)

            elif instance.sheet_title.slug == "orders-categories":
                top_categories_donut(user, dashboard_data)
                top_worst_categories_table(user, dashboard_data)
                categories_base_stat(user, dashboard_data)
                top_categories_table(user, dashboard_data)

            elif instance.sheet_title.slug == "day":
                base_statistic_card(user, dashboard_data)
                dynamic_orders_week(user, dashboard_data)

            elif instance.sheet_title.slug == "week":
                weekly_report_dynamic_orders(user, dashboard_data)
                weekly_report_goto(user, dashboard_data)
                weekly_report_orders(user, dashboard_data)
                weekly_report_sold(user, dashboard_data)

            elif instance.sheet_title.slug == "month":
                monthly_report_dynamic_orders(user, dashboard_data)
                monthly_report_goto(user, dashboard_data)
                monthly_report_orders(user, dashboard_data)
                monthly_report_sold(user, dashboard_data)

            elif instance.sheet_title.slug == "profitability":
                top_profit_profitability(user, dashboard_data)
                worst_profit_profitability(user, dashboard_data)
                base_stat_profitability(user, dashboard_data)

            elif instance.sheet_title.slug == "liquidity":
                liquidity_stat(user, dashboard_data, RentDays, "rent_days")
                liquidity_stat(user, dashboard_data, RentRemains, "rent_remains")
                liquidity_stat(user, dashboard_data, LiquidRemains, "liquid_remains")
                liquidity_stat(user, dashboard_data, LiquidRent, "liquid_rent")

            elif instance.sheet_title.slug == "abc":
                abc_stat(user, dashboard_data, ABCRent, "profit")
                abc_stat(user, dashboard_data, ABCDays, "days")
                abc_stat(user, dashboard_data, ABCConclusion, "abc")

        return instance


class DashboardTopOrdersTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopOrdersTable
        fields = ["article", "nomenclature", "orders_amount", "orders_rub"]


class DashboardTopOrdersGraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopOrdersGraph
        fields = ["name", "data"]


class DashboardTopBrandsTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBrandsTable
        fields = ["id", "brand", "orders_amount"]


class DashboardBaseStatisticCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseStatisticCard
        fields = ["orders_amount", "increase_amount", "orders_rub", "increase_rub", "orders_sells", "increase_sells"]


class DashboardTopCategoriesDonutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopCategoriesDonut
        fields = ["category", "orders_rub"]


class WeeklyReportDynamicOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyReportDynamicOrders
        fields = ["dates", "orders_data", "sold_data"]


class WeeklyReportGotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyReportGoto
        fields = ["orders_rub", "realize", "logistic", "sold"]


class WeeklyReportOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyReportOrders
        fields = ["orders_count", "percent_fact"]


class WeeklyReportSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyReportSold
        fields = ["sold_count", "percent_fact"]


class MonthlyReportDynamicOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyReportDynamicOrders
        fields = ["dates", "orders_data", "sold_data"]


class MonthlyReportGotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyReportGoto
        fields = ["orders_rub", "realize", "logistic", "sold"]


class MonthlyReportOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyReportOrders
        fields = ["orders_count", "percent_fact"]


class MonthlyReportSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyReportSold
        fields = ["sold_count", "percent_fact"]


class GraphTopWorstCategoriesTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopWorstCategoriesTable
        fields = ["id", "name", "orders_rub"]


class CategoriesBaseStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesBaseStat
        fields = ["overall", "overall_last_day", "count"]


class TopCategoriesTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopCategoriesTable
        fields = ["name", "data"]


class TopProfitProfitabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TopProfitProfitability
        fields = ["name", "data"]


class WorstProfitProfitabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorstProfitProfitability
        fields = ["name", "data"]


class BaseStatProfitabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseStatProfitability
        fields = ["op", "average_profit", "prime_cost", "logistics", "storage"]


class BaseStatDynamicOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseStatDynamicOrders
        fields = ["orders_count", "orders_rub", "orders_rows", "orders_zero"]


class DynamicOrdersWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicOrdersWeek
        fields = ["id", "date", "data"]


class RentDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentDays
        fields = ["data", "values"]


class RentRemainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentRemains
        fields = ["data", "values"]


class LiquidRemainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiquidRemains
        fields = ["data", "values"]


class LiquidRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiquidRent
        fields = ["data", "values"]


class ABCRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABCRent
        fields = ["data", "values"]


class ABCDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABCDays
        fields = ["data", "values"]


class ABCConclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABCConclusion
        fields = ["data", "values"]


class SelfSellSerializer(serializers.ModelSerializer):
    last_selfsell = serializers.DateTimeField(read_only=True, format="%Y-%m-%d", source="date")

    class Meta:
        model = SelfSell
        fields = ["id", "nm_id", "article",
                  "total_sum", "total_amount", "last_selfsell"]

    def create(self, validated_data):
        user_id = self.initial_data.get('user_id')

        nm_id = self.initial_data.get("nm_id")
        article = self.initial_data.get("article")
        total_sum = self.initial_data.get("total_sum")
        total_amount = self.initial_data.get("total_amount")
        date = self.initial_data.get("date")
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        instance = SelfSell.objects.create(
            nm_id=nm_id,
            article=article,
            total_sum=total_sum,
            total_amount=total_amount,
            date=date,
            user_id=user_id
        )
        instance.save()
        return instance
