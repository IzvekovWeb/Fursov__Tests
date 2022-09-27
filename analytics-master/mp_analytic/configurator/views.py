from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import UserSerializer, SpreadsheetSerializer, UserViewSerializer, RefreshTokenSerializer, \
    SheetViewSerializer, SheetUpdateSerializer, DashboardTopOrdersTableSerializer, \
    DashboardTopOrdersGraphSerializer, DashboardTopBrandsTableSerializer, \
    DashboardBaseStatisticCardSerializer, DashboardTopCategoriesDonutSerializer, \
    WeeklyReportSoldSerializer, WeeklyReportGotoSerializer, \
    WeeklyReportOrdersSerializer, WeeklyReportDynamicOrdersSerializer, MonthlyReportSoldSerializer, \
    MonthlyReportOrdersSerializer, MonthlyReportGotoSerializer, MonthlyReportDynamicOrdersSerializer, \
    GraphTopWorstCategoriesTableSerializer, TopCategoriesTableSerializer, CategoriesBaseStatSerializer, \
    TopProfitProfitabilitySerializer, WorstProfitProfitabilitySerializer, BaseStatProfitabilitySerializer, \
    DynamicOrdersWeekSerializer, BaseStatDynamicOrdersSerializer, RentRemainsSerializer, RentDaysSerializer, \
    LiquidRemainsSerializer, LiquidRentSerializer, ABCRentSerializer, ABCDaysSerializer, ABCConclusionSerializer, \
    SingleSheetViewSerializer, RequestConfirmCodeSerializer, ConfirmCodeSerializer, TokensSerializer, SelfSellSerializer
from .utils import get_object_plan, put_plan, get_queryset_dynamic_report_dashboard, \
    get_object_dynamic_report_dashboard, collect_self_sell_data


class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestConfirmCodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def put(self, request):
        serializer = RequestConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            instance, message = serializer.update(self.get_object(), request.data)

            return Response(status=status.HTTP_200_OK, data=message)
        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ConfirmCodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def put(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.update(self.get_object(), request.data)
            # serializer.save()
            return Response(status=status.HTTP_200_OK)
        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckWBAuthTokenAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.token_v3:
            return Response(status=status.HTTP_200_OK, data=True)
        else:
            return Response(status=status.HTTP_200_OK, data=False)


class TokensAPIView(generics.ListAPIView,
                    generics.UpdateAPIView):
    serializer_class = TokensSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        user_creds = UserCredentials.objects.filter(user=user.pk)
        instances = []
        for user_cred in user_creds:
            if not user_cred.token or not user_cred.x64key:
                instances.append(user_cred)
        return instances

    def put(self, request, *args, **kwargs):
        user_creds = self.get_queryset()
        serializer = TokensSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.update(user_creds, request.data)
            return Response(status=status.HTTP_200_OK)
        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=err)


class UserAPIView(generics.RetrieveAPIView,
                  generics.RetrieveUpdateAPIView):
    serializer_class = UserViewSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def post(self, request):
        full_name = request.data.pop("full_name", None)
        phone_num = request.data.pop("phone_num", None)

        user = request.user

        if full_name:
            user.full_name = full_name
        if phone_num:
            user.phone_num = phone_num
        if not full_name and not phone_num:
            return Response({"message": "Nothing changed"})

        user.save()
        return Response({"message": "Success!"})


class UserLogoutAPIView(generics.GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpreadsheetCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SpreadsheetSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.create(kwargs)
        return Response(status=status.HTTP_201_CREATED)


class SheetAPIView(generics.ListAPIView):
    serializer_class = SheetViewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk

        spreadsheets = Spreadsheet.objects.filter(user_id=user_id)
        if not spreadsheets:
            return None

        queryset = []
        for spreadsheet in spreadsheets:
            user_sheet = UserSheet.objects.filter(spreadsheet_id=spreadsheet.pk)
            queryset.extend(user_sheet)

        def sort_key(report):
            return report.pk

        queryset.sort(key=sort_key)

        return queryset


class SingleSheetAPIView(generics.RetrieveAPIView):
    serializer_class = SingleSheetViewSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user_id = self.request.user.pk

        slug = self.kwargs.get("slug")

        spreadsheets = Spreadsheet.objects.filter(user_id=user_id)
        if not spreadsheets:
            return None

        for spreadsheet in spreadsheets:
            user_sheets = UserSheet.objects.filter(spreadsheet_id=spreadsheet.pk)
            for user_sheet in user_sheets:
                if user_sheet.sheet_title.slug == slug:
                    return user_sheet
        return None


class SheetUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = SheetUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        sheet_id = self.kwargs.get("pk")
        user_id = self.request.user.pk

        sheet = UserSheet.objects.filter(pk=sheet_id)

        sheet = sheet.first()

        if not sheet:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        spreadsheets = Spreadsheet.objects.filter(user_id=user_id)

        for spreadsheet in spreadsheets:
            if sheet.spreadsheet.pk == spreadsheet.pk:
                return sheet

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        model_object = self.get_object()
        serializer: SheetUpdateSerializer = self.get_serializer(model_object, data=request.data)
        while True:
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            except PermissionError:
                continue
            except Exception as err:
                print(err)
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class DashboardTopOrdersTableAPIView(generics.ListAPIView):
    serializer_class = DashboardTopOrdersTableSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_queryset_dynamic_report_dashboard(TopOrdersTable, self.request)


class DashboardTopOrdersGraphAPIView(generics.ListAPIView):
    serializer_class = DashboardTopOrdersGraphSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_queryset_dynamic_report_dashboard(TopOrdersGraph, self.request)


class TopBrandsTableAPIView(generics.ListAPIView):
    serializer_class = DashboardTopBrandsTableSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_queryset_dynamic_report_dashboard(TopBrandsTable, self.request)


class BaseStatisticCardAPIView(generics.RetrieveAPIView):
    serializer_class = DashboardBaseStatisticCardSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(BaseStatisticCard, self.request)


class TopCategoriesDonutAPIView(generics.RetrieveAPIView):
    serializer_class = DashboardTopCategoriesDonutSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(TopCategoriesDonut, self.request)


class WeeklyReportDynamicOrdersAPIView(generics.RetrieveAPIView):
    serializer_class = WeeklyReportDynamicOrdersSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(WeeklyReportDynamicOrders, self.request)


class WeeklyReportGotoAPIView(generics.RetrieveAPIView):
    serializer_class = WeeklyReportGotoSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(WeeklyReportGoto, self.request)


class WeeklyReportOrdersAPIView(generics.RetrieveAPIView):
    serializer_class = WeeklyReportOrdersSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(WeeklyReportOrders, self.request)


class WeeklyReportSoldAPIView(generics.RetrieveAPIView):
    serializer_class = WeeklyReportSoldSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(WeeklyReportSold, self.request)


class MonthlyReportDynamicOrdersAPIView(generics.RetrieveAPIView):
    serializer_class = MonthlyReportDynamicOrdersSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(MonthlyReportDynamicOrders, self.request)


class MonthlyReportGotoAPIView(generics.RetrieveAPIView):
    serializer_class = MonthlyReportGotoSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(MonthlyReportGoto, self.request)


class MonthlyReportOrdersAPIView(generics.RetrieveAPIView):
    serializer_class = MonthlyReportOrdersSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(MonthlyReportOrders, self.request)


class MonthlyReportSoldAPIView(generics.RetrieveAPIView):
    serializer_class = MonthlyReportSoldSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(MonthlyReportSold, self.request)


class GraphTopWorstCategoriesTableAPIView(generics.ListAPIView):
    serializer_class = GraphTopWorstCategoriesTableSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_queryset_dynamic_report_dashboard(TopWorstCategoriesTable, self.request)


class CategoriesBaseStatAPIView(generics.RetrieveAPIView):
    serializer_class = CategoriesBaseStatSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(CategoriesBaseStat, self.request)


class TopCategoriesTableAPIView(generics.ListAPIView):
    serializer_class = TopCategoriesTableSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_queryset_dynamic_report_dashboard(TopCategoriesTable, self.request)


class TopProfitProfitabilityAPIView(generics.RetrieveAPIView):
    serializer_class = TopProfitProfitabilitySerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(TopProfitProfitability, self.request)


class WorstProfitProfitabilityAPIView(generics.RetrieveAPIView):
    serializer_class = WorstProfitProfitabilitySerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(WorstProfitProfitability, self.request)


class BaseStatProfitabilityAPIView(generics.RetrieveAPIView):
    serializer_class = BaseStatProfitabilitySerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(BaseStatProfitability, self.request)


class DynamicOrdersWeekAPIView(generics.ListAPIView):
    serializer_class = DynamicOrdersWeekSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_queryset_dynamic_report_dashboard(DynamicOrdersWeek, self.request)


class BaseStatDynamicOrdersAPIView(generics.RetrieveAPIView):
    serializer_class = BaseStatDynamicOrdersSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(BaseStatDynamicOrders, self.request)


class RentDaysAPIView(generics.RetrieveAPIView):
    serializer_class = RentDaysSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(RentDays, self.request)


class RentRemainsAPIView(generics.RetrieveAPIView):
    serializer_class = RentRemainsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(RentRemains, self.request)


class LiquidRemainsAPIView(generics.RetrieveAPIView):
    serializer_class = LiquidRemainsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(LiquidRemains, self.request)


class LiquidRentAPIView(generics.RetrieveAPIView):
    serializer_class = LiquidRentSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(LiquidRent, self.request)


class ABCRentAPIView(generics.RetrieveAPIView):
    serializer_class = ABCRentSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(ABCRent, self.request)


class ABCDaysAPIView(generics.RetrieveAPIView):
    serializer_class = ABCDaysSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(ABCDays, self.request)


class ABCConclusionAPIView(generics.RetrieveAPIView):
    serializer_class = ABCConclusionSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_dynamic_report_dashboard(ABCConclusion, self.request)


class WeekPlanUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_plan(self.request)

    def put(self, request, **kwargs):
        return put_plan(self.get_object, Response, request, status, 1)


class MonthPlanUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_plan(self.request)

    def put(self, request, **kwargs):
        return put_plan(self.get_object, Response, request, status, 4)


class SelfSellAPIView(generics.ListAPIView,
                      generics.CreateAPIView):
    serializer_class = SelfSellSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return SelfSell.objects.filter(user_id=user.pk)

    def post(self, request, *args, **kwargs):
        request.data["user_id"] = request.user.pk
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class SelfSellStatAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = SelfSell.objects.filter(user_id=user.pk)

        data = {
            "total_sum": 0,
            "total_amount": 0,
            "article": "",
            "article_total": 0,
        }
        if not len(queryset):
            return Response(status=status.HTTP_200_OK, data=data)
        try:
            collect_self_sell_data(queryset, data)
            return Response(status=status.HTTP_200_OK, data=data)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
