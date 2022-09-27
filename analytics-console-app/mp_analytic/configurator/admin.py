from django.contrib import admin
from .models import User, Tariff, UserSheet, Sheet, Spreadsheet


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "full_name", "is_superuser", "is_staff")


@admin.register(UserSheet)
class UserAdmin(admin.ModelAdmin):
    list_display = ("sheet_title", "update_at", "spreadsheet", "sheet_id")


@admin.register(Tariff)
class UserAdmin(admin.ModelAdmin):
    list_display = ("title", )


@admin.register(Sheet)
class UserAdmin(admin.ModelAdmin):
    list_display = ("title", "tariff")


@admin.register(Spreadsheet)
class UserAdmin(admin.ModelAdmin):
    list_display = ("spreadsheet_title", "user", "spreadsheet_id")
