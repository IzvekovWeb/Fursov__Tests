from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Spreadsheet, UserSheet
from .serializers import UserSerializer, SpreadsheetSerializer, UserViewSerializer, RefreshTokenSerializer, \
    SheetViewSerializer, SheetUpdateSerializer


class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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


class SpreadsheetCreateAPIView(generics.CreateAPIView):
    serializer_class = SpreadsheetSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs.get('pk'))


class SheetAPIView(generics.ListAPIView):
    serializer_class = SheetViewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        user_id = user.pk

        spreadsheets = Spreadsheet.objects.filter(user_id=user_id)
        if not spreadsheets:
            return None

        queryset = []
        for spreadsheet in spreadsheets:
            user_sheet = UserSheet.objects.filter(spreadsheet_id=spreadsheet.pk)
            queryset.extend(user_sheet)

        return queryset


class SheetUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = SheetUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        sheet_id = self.kwargs.get("pk")
        sheet = UserSheet.objects.filter(pk=sheet_id)
        return sheet.first()
