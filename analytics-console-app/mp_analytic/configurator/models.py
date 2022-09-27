from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=254, verbose_name='email address', unique=True)
    phone_num = models.CharField(max_length=20, null=True, blank=True)
    date_follow = models.DateTimeField(null=True, blank=True)
    date_expire = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    tariff = models.ForeignKey("Tariff", on_delete=models.SET_NULL, null=True, blank=True)
    last_login = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.full_name} - {self.is_active}"


class Tariff(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "tariff"
        verbose_name_plural = "tariffs"


class Sheet(models.Model):
    title = models.CharField(max_length=127)
    tariff = models.ForeignKey("Tariff", on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "sheet"
        verbose_name_plural = "sheets"


class Spreadsheet(models.Model):
    spreadsheet_id = models.CharField(max_length=127)
    spreadsheet_title = models.CharField(max_length=64)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return self.spreadsheet_title

    class Meta:
        verbose_name = "spreadsheet"
        verbose_name_plural = "spreadsheets"


class UserSheet(models.Model):
    spreadsheet = models.ForeignKey("Spreadsheet", on_delete=models.CASCADE)
    sheet_id = models.CharField(max_length=64)
    sheet_title = models.ForeignKey("Sheet", on_delete=models.CASCADE)
    update_at = models.DateTimeField(null=True, blank=True, default=None)
    favourite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sheet_title} - {self.update_at}"

    class Meta:
        verbose_name = "user_sheet"
        verbose_name_plural = "user_sheets"
