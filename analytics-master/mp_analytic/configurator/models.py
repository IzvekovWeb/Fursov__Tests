from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=254, verbose_name='email address', unique=True)
    phone_num = models.CharField(max_length=20, null=True, blank=True)
    date_follow = models.DateTimeField(null=True, blank=True)
    date_expire = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    tariff = models.ForeignKey("Tariff", to_field="title", default="Оптимальный",
                               on_delete=models.SET_NULL, null=True, blank=True)
    token_v3 = models.TextField(verbose_name="WildV3Token", null=True, blank=True, default=None, unique=True)
    last_login = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.full_name} - {self.is_active}"


class UserCredentials(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    wb_token = models.CharField(max_length=127, null=True, blank=True, default=True)
    name = models.CharField(max_length=127, null=True, blank=True, default=True)
    organization = models.CharField(max_length=127, null=True, blank=True, default=True)
    token = models.CharField(max_length=255, null=True, blank=True, default=True)
    x64key = models.CharField(max_length=64, null=True, blank=True, default=True)
    supplier_id = models.CharField(max_length=127, null=True, blank=True, default=True)


class Tariff(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "tariff"
        verbose_name_plural = "tariffs"


class Sheet(models.Model):
    title = models.CharField(max_length=127)
    google_title = models.CharField(max_length=127, blank=True, default=None, null=True, unique=True)
    slug = models.CharField(max_length=64, blank=True, default=None, null=True, unique=True)
    has_detail = models.BooleanField(default=False)
    secondary = models.BooleanField(default=False)
    tariff = models.ForeignKey("Tariff", on_delete=models.PROTECT)
    description = models.TextField(blank=True, default=None, null=True)

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


class TopOrdersTable(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="dynamic-art-count", on_delete=models.CASCADE)

    article = models.CharField(max_length=64, verbose_name="Артикул", null=True, blank=True, default=None)
    nomenclature = models.CharField(max_length=24, verbose_name="Номенклатура", null=True, blank=True, default=None)
    orders_amount = models.IntegerField(verbose_name="Заказы, штуки", null=True, blank=True, default=None)
    orders_rub = models.FloatField(verbose_name="Заказы, рубли", null=True, blank=True, default=None)

    def __str__(self):
        return f"Топ 10 заказываемых артикулов за неделю"


class TopOrdersGraph(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="dynamic-art-count", on_delete=models.CASCADE)

    name = models.CharField(max_length=64, verbose_name="Артикул", null=True, blank=True, default=None)
    data = ArrayField(models.IntegerField(verbose_name="Заказы, штуки", null=True, blank=True, default=None), size=7,
                      blank=True, null=True)

    def __str__(self):
        return f"Топ 5 заказываемых артикулов в течение недели"


class TopBrandsTable(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="dynamic-art-count", on_delete=models.CASCADE)

    brand = models.CharField(max_length=127, verbose_name="Бренд", null=True, blank=True, default=None)
    orders_amount = models.IntegerField(verbose_name="Заказы, штуки", null=True, blank=True, default=None)

    def __str__(self):
        return f"Топ 5 заказываемых брендов"


class TopWorstCategoriesTable(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="orders-categories", on_delete=models.CASCADE)

    name = models.CharField(max_length=127, verbose_name="Категория", null=True, blank=True, default=None)
    orders_rub = models.IntegerField(verbose_name="Заказы, рубли", null=True, blank=True, default=None)

    def __str__(self):
        return f"Топ 5 худших категорий"


class CategoriesBaseStat(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="orders-categories", on_delete=models.CASCADE)

    overall = models.IntegerField(verbose_name="Итого", null=True, blank=True, default=None)
    overall_last_day = models.IntegerField(verbose_name="Итого за последний день", null=True, blank=True, default=None)
    count = models.IntegerField(verbose_name="Количество категорий", null=True, blank=True, default=None)

    def __str__(self):
        return f"Статистика по категориям"


class TopCategoriesTable(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="orders-categories", on_delete=models.CASCADE)

    name = models.CharField(max_length=127, verbose_name="Категория", null=True, blank=True, default=None)
    data = ArrayField(models.IntegerField(verbose_name="Заказы, рубли.", null=True, blank=True, default=None),
                      blank=True, size=6, null=True)

    def __str__(self):
        return f"Топ 5 лучших категорий в срезе недели"


class TopCategoriesDonut(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="orders-categories", on_delete=models.CASCADE)

    category = ArrayField(
        models.CharField(max_length=64, verbose_name="Категория", null=True, blank=True, default=None), blank=True,
        size=6, null=True)

    orders_rub = ArrayField(models.IntegerField(verbose_name="Заказы, рубли.", null=True, blank=True, default=None),
                            blank=True, size=6, null=True)

    def __str__(self):
        return f"Топ 5 заказываемых категорий"


class BaseStatisticCard(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="day", on_delete=models.CASCADE)

    orders_amount = models.IntegerField(verbose_name="Заказы, штуки", null=True, blank=True, default=None)
    increase_amount = models.IntegerField(verbose_name="Прирост/убыток заказов в количестве", null=True, blank=True,
                                          default=None)

    orders_rub = models.FloatField(verbose_name="Заказы, рубли", null=True, blank=True, default=None)
    increase_rub = models.IntegerField(verbose_name="Прирост/убыток заказов в рублях", null=True, blank=True,
                                       default=None)

    orders_sells = models.IntegerField(verbose_name="Продажи, рубли", null=True, blank=True, default=None)
    increase_sells = models.IntegerField(verbose_name="Прирост/убыток продаж", null=True, blank=True, default=None)

    def __str__(self):
        return f"Сводка статистики за неделю"


class WeeklyReportDynamicOrders(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="week", on_delete=models.CASCADE)

    dates = ArrayField(models.CharField(max_length=20, verbose_name="Дата", null=True, blank=True, default=None),
                       blank=True, size=6, null=True)
    orders_data = ArrayField(models.IntegerField(verbose_name="Заказы, штуки", null=True, blank=True, default=None),
                             blank=True, size=6, null=True)
    sold_data = ArrayField(models.IntegerField(verbose_name="Продажи, штуки", null=True, blank=True, default=None),
                           blank=True, size=6, null=True)

    def __str__(self):
        return f"Сводка анализа заказов в течение недели"


class WeeklyReportGoto(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="week", on_delete=models.CASCADE)

    realize = models.IntegerField(verbose_name="К перечислению", null=True, blank=True, default=None)
    orders_rub = models.FloatField(verbose_name="Заказы, рубли", null=True, blank=True, default=None)
    logistic = models.FloatField(verbose_name="Выкуп, рубли", null=True, blank=True, default=None)
    sold = models.FloatField(verbose_name="Логистика, рубли", null=True, blank=True, default=None)

    def __str__(self):
        return f"Сводка анализа планирования за неделю"


class WeeklyReportOrders(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="week", on_delete=models.CASCADE)

    orders_count = models.IntegerField(verbose_name="Заказы, штуки", null=True, blank=True, default=None)
    percent_fact = models.IntegerField(verbose_name="Сделано", null=True, blank=True, default=None)

    def __str__(self):
        return f"Сводка анализа заказов за неделю"


class WeeklyReportSold(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="week", on_delete=models.CASCADE)

    sold_count = models.IntegerField(verbose_name="Выкуп, штуки", null=True, blank=True, default=None)
    percent_fact = models.IntegerField(verbose_name="Сделано", null=True, blank=True, default=None)

    def __str__(self):
        return f"Сводка анализа выкупов за неделю"


class MonthlyReportDynamicOrders(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="month", on_delete=models.CASCADE)

    dates = ArrayField(models.CharField(max_length=20, verbose_name="Дата", null=True, blank=True, default=None),
                       blank=True, size=6, null=True)
    orders_data = ArrayField(models.IntegerField(verbose_name="Заказы, штуки", null=True, blank=True, default=None),
                             blank=True, size=6, null=True)
    sold_data = ArrayField(models.IntegerField(verbose_name="Продажи, штуки", null=True, blank=True, default=None),
                           blank=True, size=6, null=True)

    def __str__(self):
        return f"Сводка анализа заказов в течение месяца"


class MonthlyReportGoto(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="month", on_delete=models.CASCADE)

    realize = models.IntegerField(verbose_name="К перечислению", null=True, blank=True, default=None)
    orders_rub = models.FloatField(verbose_name="Заказы, рубли", null=True, blank=True, default=None)
    logistic = models.FloatField(verbose_name="Выкуп, рубли", null=True, blank=True, default=None)
    sold = models.FloatField(verbose_name="Логистика, рубли", null=True, blank=True, default=None)

    def __str__(self):
        return f"Сводка анализа планирования за месяц"


class MonthlyReportOrders(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="month", on_delete=models.CASCADE)

    orders_count = models.IntegerField(verbose_name="Заказы, штуки", null=True, blank=True, default=None)
    percent_fact = models.IntegerField(verbose_name="Сделано", null=True, blank=True, default=None)

    def __str__(self):
        return f"Сводка анализа заказов за месяц"


class MonthlyReportSold(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="month", on_delete=models.CASCADE)

    sold_count = models.IntegerField(verbose_name="Выкуп, штуки", null=True, blank=True, default=None)
    percent_fact = models.IntegerField(verbose_name="Сделано", null=True, blank=True, default=None)

    def __str__(self):
        return f"Сводка анализа выкупов за месяц"


class ProfitabilityBaseModel(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="profitability", on_delete=models.CASCADE)

    name = ArrayField(models.CharField(max_length=127, verbose_name="Артикул", null=True, blank=True, default=None),
                      blank=True, size=24, null=True)
    data = ArrayField(models.IntegerField(verbose_name="Прибыль на 1 шт", null=True, blank=True, default=None),
                      blank=True, size=24, null=True)


class TopProfitProfitability(ProfitabilityBaseModel):
    def __str__(self):
        return f"Топ-20 прибыльных товаров"


class WorstProfitProfitability(ProfitabilityBaseModel):
    def __str__(self):
        return f"Топ-20 неприбыльных товаров"


class BaseStatProfitability(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="profitability", on_delete=models.CASCADE)

    op = models.IntegerField(verbose_name="Операционная прибыль", null=True, blank=True, default=None)
    average_profit = models.IntegerField(verbose_name="Средняя прибыль за 1 шт", null=True, blank=True, default=None)
    prime_cost = models.IntegerField(verbose_name="Себестоимость", null=True, blank=True, default=None)
    logistics = models.IntegerField(verbose_name="Логистика", null=True, blank=True, default=None)
    storage = models.IntegerField(verbose_name="Хранение", null=True, blank=True, default=None)

    def __str__(self):
        return f"Базовая статистика по рентабельности"


class BaseStatDynamicOrders(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="dynamic-art-count", on_delete=models.CASCADE)

    orders_count = models.IntegerField(verbose_name="Заказано, штуки", null=True, blank=True, default=None)
    orders_rub = models.IntegerField(verbose_name="Заказано, рубли", null=True, blank=True, default=None)
    orders_rows = models.IntegerField(verbose_name="Товаров", null=True, blank=True, default=None)
    orders_zero = models.IntegerField(verbose_name="Товар без заказов", null=True, blank=True, default=None)

    def __str__(self):
        return f"Базовая статистика по заказам за неделю"


class DynamicOrdersWeek(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="day", on_delete=models.CASCADE)

    date = models.CharField(max_length=24, verbose_name="Дата", null=True, blank=True, default=None)
    data = models.IntegerField(verbose_name="Заказано, рубли", null=True, blank=True, default=None)

    def __str__(self):
        return f"Таблица заказов в течение недели"


class LiquidityBaseModel(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="liquidity", on_delete=models.CASCADE)

    data = ArrayField(models.CharField(max_length=64, null=True, blank=True, default=None),
                      blank=True, size=6, null=True)
    values = ArrayField(models.FloatField(null=True, blank=True, default=None),
                        blank=True, size=6, null=True)


class RentDays(LiquidityBaseModel):
    def __str__(self):
        return "Категория рентабельности, % - Оборачиваемость, дни"


class RentRemains(LiquidityBaseModel):
    def __str__(self):
        return "Категория рентабельности, % - Процент остатков, руб"


class LiquidRemains(LiquidityBaseModel):
    def __str__(self):
        return "Категория ликвидности, дни - Процент остатоков, руб"


class LiquidRent(LiquidityBaseModel):
    def __str__(self):
        return "Категория ликвидности, дни - Рентабельность, %"


class ABCBaseModel(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet_title = models.ForeignKey("Sheet", to_field="slug", default="abc", on_delete=models.CASCADE)

    data = ArrayField(models.CharField(max_length=7, null=True, blank=True, default=None),
                      blank=True, size=4, null=True)
    values = ArrayField(models.IntegerField(null=True, blank=True, default=None),
                        blank=True, size=4, null=True)


class ABCRent(ABCBaseModel):
    def __str__(self):
        return "ABC Рентабельность"


class ABCDays(ABCBaseModel):
    def __str__(self):
        return "ABC Оборачиваемость"


class ABCConclusion(ABCBaseModel):
    def __str__(self):
        return "ABC Итог"


class SelfSell(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    nm_id = models.CharField(max_length=64, verbose_name="Номенклатура", null=True, blank=True, default=None)
    article = models.CharField(max_length=128, verbose_name="Артикул", null=True, blank=True, default=None)
    total_amount = models.IntegerField(verbose_name="Выкупы, шт", null=True, blank=True, default=None)
    total_sum = models.SmallIntegerField(verbose_name="Выкупы, рубли", null=True, blank=True, default=None)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Номенклатура: {nm_id} - Дата: {date} Сумма выкупа: {total_sum}"

