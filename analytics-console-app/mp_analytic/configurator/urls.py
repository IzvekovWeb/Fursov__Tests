from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from configurator import views
from .views import UserRegisterAPIView

urlpatterns = [
    path("register", UserRegisterAPIView.as_view(), name="register"),
    path("logout", views.UserLogoutAPIView.as_view(), name='logout'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('user', views.UserAPIView.as_view(), name='user'),

    path("create/<int:pk>", views.SpreadsheetCreateAPIView.as_view(), name='spreadsheets'),
    path("analytic/wildberries", views.SheetAPIView.as_view(), name="sheet"),
    path("analytic/wildberries/refresh/<int:pk>", views.SheetUpdateAPIView.as_view(), name="refresh_sheet"),
]
