from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from configurator import views

urlpatterns = [
    path("register", views.UserRegisterAPIView.as_view(), name="register"),
    path("request-confirm", views.RequestConfirmCodeAPIView.as_view(), name="request_confirm"),
    path("confirm-code", views.ConfirmCodeAPIView.as_view(), name="confirm_code"),
    path("wb-tokens", views.TokensAPIView.as_view(), name="wb_tokens"),
    path("check-wb-auth-token", views.CheckWBAuthTokenAPIView.as_view(), name="check_wb_auth_token"),

    path("logout", views.UserLogoutAPIView.as_view(), name='logout'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('user', views.UserAPIView.as_view(), name='user'),  # Profile

    path("create/<int:pk>", views.SpreadsheetCreateAPIView.as_view(), name='spreadsheets'),  # Create empty Spreadsheets
    path("analytic/wildberries", views.SheetAPIView.as_view(), name="sheet"),  # List of reports
    path("analytic/wildberries/refresh/<int:pk>", views.SheetUpdateAPIView.as_view(), name="refresh_sheet"),
    # Update report

    # DASHBOARD
    path("analytic/dashboard/top-orders-table", views.DashboardTopOrdersTableAPIView.as_view(),
         name="top_orders_table"),  # Dashboard Top Orders Table

    path("analytic/dashboard/top-orders-graph", views.DashboardTopOrdersGraphAPIView.as_view(),
         name="top_orders_graph"),  # Dashboard Top Orders Graph

    path("analytic/dashboard/top-brands-table", views.TopBrandsTableAPIView.as_view(),
         name="top_brand_table"),  # Dashboard Top Brands

    path("analytic/dashboard/base-statistic", views.BaseStatisticCardAPIView.as_view(),
         name="base_statistic"),  # Dashboard Base Statistics

    path("analytic/dashboard/top-categories-donut", views.TopCategoriesDonutAPIView.as_view(),
         name="top_categories_donut"),  # Dashboard Top Categories Donut

    # WEEKLY DYNAMIC
    path("analytic/wildberries/weekly-report-dynamic-orders", views.WeeklyReportDynamicOrdersAPIView.as_view(),
         name="weekly_report_dynamic_orders"),  # Weekly Report Orders' Dynamic

    path("analytic/wildberries/weekly-report-goto", views.WeeklyReportGotoAPIView.as_view(),
         name="weekly_report_goto"),  # Weekly Report GoTo

    path("analytic/wildberries/weekly-report-orders", views.WeeklyReportOrdersAPIView.as_view(),
         name="weekly_report_orders"),  # Weekly Report Orders

    path("analytic/wildberries/weekly-report-sold", views.WeeklyReportSoldAPIView.as_view(),
         name="weekly_report_sold"),  # Weekly Report Sold

    # MONTHLY DYNAMIC
    path("analytic/wildberries/monthly-report-dynamic-orders", views.MonthlyReportDynamicOrdersAPIView.as_view(),
         name="monthly_report_dynamic_orders"),  # Monthly Report Orders' Dynamic

    path("analytic/wildberries/monthly-report-goto", views.MonthlyReportGotoAPIView.as_view(),
         name="monthly_report_goto"),  # Monthly Report GoTo

    path("analytic/wildberries/monthly-report-orders", views.MonthlyReportOrdersAPIView.as_view(),
         name="monthly_report_orders"),  # Monthly Report Orders

    path("analytic/wildberries/monthly-report-sold", views.MonthlyReportSoldAPIView.as_view(),
         name="monthly_report_sold"),  # Monthly Report Sold

    # WEEK's PLAN UPDATE
    path("analytic/wildberries/week-plan-update", views.WeekPlanUpdateAPIView.as_view(), name="week_plan_update"),

    # MONTH's PLAN UPDATE
    path("analytic/wildberries/month-plan-update", views.MonthPlanUpdateAPIView.as_view(), name="month_plan_update"),

    path("analytic/wildberries/top-worst-categories", views.GraphTopWorstCategoriesTableAPIView.as_view(),
         name="top_worst_categories"),
    path("analytic/wildberries/top-categories-graph", views.TopCategoriesTableAPIView.as_view(),
         name="top_categories_graph"),
    path("analytic/wildberries/categories-base-stat", views.CategoriesBaseStatAPIView.as_view(),
         name="categories_base_stat"),

    # TOP and WORST articles by profit
    path("analytic/wildberries/top-profit-profitability", views.TopProfitProfitabilityAPIView.as_view(),
         name="top_profit_profitability"),
    path("analytic/wildberries/worst-profit-profitability", views.WorstProfitProfitabilityAPIView.as_view(),
         name="worst_profit_profitability"),
    path("analytic/wildberries/base-stat-profitability", views.BaseStatProfitabilityAPIView.as_view(),
         name="base_stat_profitability"),

    # DYNAMIC ORDERS
    path("analytic/wildberries/base-stat-dynamic-orders", views.BaseStatDynamicOrdersAPIView.as_view(),
         name="base_stat_dynamic_orders"),
    path("analytic/wildberries/dynamic-orders-week", views.DynamicOrdersWeekAPIView.as_view(),
         name="dynamic_orders_week"),

    # LIQUIDITY
    path("analytic/wildberries/liquidity/rent-days", views.RentDaysAPIView.as_view(), name="rent_days"),
    path("analytic/wildberries/liquidity/rent-remains", views.RentRemainsAPIView.as_view(), name="rent_remains"),
    path("analytic/wildberries/liquidity/liquid-remains", views.LiquidRemainsAPIView.as_view(), name="liquid_remains"),
    path("analytic/wildberries/liquidity/liquid-rent", views.LiquidRentAPIView.as_view(), name="liquid_rent"),

    # ABC
    path("analytic/wildberries/abc/rent", views.ABCRentAPIView.as_view(), name="abc_rent"),
    path("analytic/wildberries/abc/days", views.ABCDaysAPIView.as_view(), name="abc_days"),
    path("analytic/wildberries/abc/conclusion", views.ABCConclusionAPIView.as_view(), name="abc_conclusion"),

    path("analytic/wildberries/<str:slug>", views.SingleSheetAPIView.as_view(), name="report_slug"),

    path("selfsell", views.SelfSellAPIView.as_view(), name="selfsell"),
    path("selfsell-stat", views.SelfSellStatAPIView.as_view(), name="selfsell_stat"),
]
