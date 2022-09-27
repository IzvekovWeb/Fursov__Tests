from domain.utils.wb_week_plan_update import insert_plan
from .models import *

SLUG = ("day", "week", "month",
        "dynamic-art-count",
        "orders-categories",
        "profitability", "abc",
        "liquidity")


def top_orders_table(user, dashboard_data):
    top_orders = TopOrdersTable.objects.filter(user=user.pk)
    if top_orders:
        top_orders.delete()

    for data in dashboard_data["topOrders"]:
        TopOrdersTable(
            user=user,
            article=data["name"],
            nomenclature=data["nmId"],
            orders_amount=data["ordersAmount"],
            orders_rub=data["ordersRub"],
        ).save()


def top_orders_graph(user, dashboard_data):
    top_orders = TopOrdersGraph.objects.filter(user=user.pk)
    if top_orders:
        top_orders.delete()

    for data in dashboard_data["topOrdersWeek"]:
        graph = TopOrdersGraph(
            user=user,
            name=data["name"],
            data=data["ordersAmount"]
        )
        graph.save()


def top_brands_table(user, dashboard_data):
    top_brands = TopBrandsTable.objects.filter(user=user.pk)
    if top_brands:
        top_brands.delete()

    for data in dashboard_data["topBrands"]:
        top_brands_graph = TopBrandsTable(
            user=user,
            brand=data["brand"],
            orders_amount=data["ordersAmount"]
        )
        top_brands_graph.save()


def base_statistic_card(user, dashboard_data):
    base_statistic = BaseStatisticCard.objects.filter(user=user.pk)
    if base_statistic:
        base_statistic.delete()

    card = BaseStatisticCard(
        user=user,

        orders_amount=dashboard_data["ordersCount"]["ordersToday"],
        increase_amount=dashboard_data["ordersCount"]["increase"],

        orders_rub=dashboard_data["ordersRub"]["ordersToday"],
        increase_rub=dashboard_data["ordersRub"]["increase"],

        orders_sells=dashboard_data["sells"]["ordersToday"],
        increase_sells=dashboard_data["sells"]["increase"],
    )
    card.save()


def top_categories_donut(user, dashboard_data):
    top_categories = TopCategoriesDonut.objects.filter(user=user.pk)
    if top_categories:
        top_categories.delete()

    donut = TopCategoriesDonut(
        user=user,
        category=dashboard_data["category"],
        orders_rub=dashboard_data["ordersRub"],
    )

    donut.save()


def top_worst_categories_table(user, dashboard_data):
    top_worst = TopWorstCategoriesTable.objects.filter(user=user.pk)
    if top_worst:
        top_worst.delete()

    for data in dashboard_data.get("worstCategories"):
        table = TopWorstCategoriesTable(
            user=user,
            name=data["name"],
            orders_rub=data["ordersRub"],
        )

        table.save()


def categories_base_stat(user, dashboard_data):
    categories = CategoriesBaseStat.objects.filter(user=user.pk)
    if categories:
        categories.delete()

    stat = CategoriesBaseStat(
        user=user,
        overall=dashboard_data["base"]["overall"],
        overall_last_day=dashboard_data["base"]["overallLastDay"],
        count=dashboard_data["base"]["count"],
    )

    stat.save()


def top_categories_table(user, dashboard_data):
    top_categories = TopCategoriesTable.objects.filter(user=user.pk)
    if top_categories:
        top_categories.delete()

    for data in dashboard_data.get("week"):
        table = TopCategoriesTable(
            user=user,
            name=data["name"],
            data=data["data"],
        )

        table.save()


def weekly_report_dynamic_orders(user, dashboard_data):
    weekly_dynamic_orders = WeeklyReportDynamicOrders.objects.filter(user=user.pk)
    if weekly_dynamic_orders:
        weekly_dynamic_orders.delete()

    data = dashboard_data["dynamicOrders"]
    dynamic_orders = WeeklyReportDynamicOrders(
        user=user,
        dates=data["dates"],
        orders_data=data["ordersData"],
        sold_data=data["soldData"],
    )
    dynamic_orders.save()


def weekly_report_goto(user, dashboard_data):
    weekly_goto = WeeklyReportGoto.objects.filter(user=user.pk)
    if weekly_goto:
        weekly_goto.delete()

    data = dashboard_data["goto"]
    goto = WeeklyReportGoto(
        user=user,
        realize=data["realize"],
        orders_rub=data["ordersRub"],
        logistic=data["logistic"],
        sold=data["sold"],
    )
    goto.save()


def weekly_report_orders(user, dashboard_data):
    weekly_orders = WeeklyReportOrders.objects.filter(user=user.pk)
    if weekly_orders:
        weekly_orders.delete()

    data = dashboard_data["orders"]
    orders = WeeklyReportOrders(
        user=user,
        orders_count=data["ordersCount"],
        percent_fact=data["percentFact"],
    )
    orders.save()


def weekly_report_sold(user, dashboard_data):
    weekly_sold = WeeklyReportSold.objects.filter(user=user.pk)
    if weekly_sold:
        weekly_sold.delete()

    data = dashboard_data["sold"]
    sold = WeeklyReportSold(
        user=user,
        sold_count=data["soldCount"],
        percent_fact=data["percentFact"],
    )
    sold.save()


def monthly_report_dynamic_orders(user, dashboard_data):
    monthly_dynamic_orders = MonthlyReportDynamicOrders.objects.filter(user=user.pk)
    if monthly_dynamic_orders:
        monthly_dynamic_orders.delete()

    data = dashboard_data["dynamicOrders"]
    dynamic_orders = MonthlyReportDynamicOrders(
        user=user,
        dates=data["dates"],
        orders_data=data["ordersData"],
        sold_data=data["soldData"],
    )
    dynamic_orders.save()


def monthly_report_goto(user, dashboard_data):
    monthly_goto = MonthlyReportGoto.objects.filter(user=user.pk)
    if monthly_goto:
        monthly_goto.delete()

    data = dashboard_data["goto"]
    goto = MonthlyReportGoto(
        user=user,
        realize=data["realize"],
        orders_rub=data["ordersRub"],
        logistic=data["logistic"],
        sold=data["sold"],
    )
    goto.save()


def monthly_report_orders(user, dashboard_data):
    monthly_orders = MonthlyReportOrders.objects.filter(user=user.pk)
    if monthly_orders:
        monthly_orders.delete()

    data = dashboard_data["orders"]
    orders = MonthlyReportOrders(
        user=user,
        orders_count=data["ordersCount"],
        percent_fact=data["percentFact"],
    )
    orders.save()


def monthly_report_sold(user, dashboard_data):
    monthly_sold = MonthlyReportSold.objects.filter(user=user.pk)
    if monthly_sold:
        monthly_sold.delete()

    data = dashboard_data["sold"]
    sold = MonthlyReportSold(
        user=user,
        sold_count=data["soldCount"],
        percent_fact=data["percentFact"],
    )
    sold.save()


def top_profit_profitability(user, dashboard_data):
    top = TopProfitProfitability.objects.filter(user=user.pk)
    if top:
        top.delete()

    profit = TopProfitProfitability(
        user=user,
        name=dashboard_data["topProfit"]["name"],
        data=dashboard_data["topProfit"]["data"],
    )
    profit.save()


def worst_profit_profitability(user, dashboard_data):
    worst = WorstProfitProfitability.objects.filter(user=user.pk)
    if worst:
        worst.delete()

    profit = WorstProfitProfitability(
        user=user,
        name=dashboard_data["worstProfit"]["name"],
        data=dashboard_data["worstProfit"]["data"],
    )
    profit.save()


def dynamic_orders_week(user, dashboard_data):
    dynamic = DynamicOrdersWeek.objects.filter(user=user.pk)
    if dynamic:
        dynamic.delete()

    for data in dashboard_data["baseStat"]:
        orders = DynamicOrdersWeek(
            user=user,
            date=data["date"],
            data=data["data"],
        )
        orders.save()


def base_stat_profitability(user, dashboard_data):
    base = BaseStatProfitability.objects.filter(user=user.pk)
    if base:
        base.delete()

    stat = BaseStatProfitability(
        user=user,
        op=dashboard_data["baseStat"]["op"],
        average_profit=dashboard_data["baseStat"]["averageProfit"],
        prime_cost=dashboard_data["baseStat"]["primeCost"],
        storage=dashboard_data["baseStat"]["storage"],
        logistics=dashboard_data["baseStat"]["logistics"],
    )
    stat.save()


def base_stat_dynamic_orders(user, dashboard_data):
    base = BaseStatDynamicOrders.objects.filter(user=user.pk)
    if base:
        base.delete()

    stat = BaseStatDynamicOrders(
        user=user,
        orders_count=dashboard_data["baseStat"]["ordersCount"],
        orders_rub=dashboard_data["baseStat"]["ordersRub"],
        orders_rows=dashboard_data["baseStat"]["ordersRows"],
        orders_zero=dashboard_data["baseStat"]["ordersZero"],
    )
    stat.save()


def liquidity_stat(user, dashboard_data, model, key):
    rent = model.objects.filter(user=user.pk)
    if rent:
        rent.delete()

    stat = model(
        user=user,
        data=dashboard_data[key]["data"],
        values=dashboard_data[key]["values"],
    )
    stat.save()


def abc_stat(user, dashboard_data, model, key):
    abc = model.objects.filter(user=user.pk)
    if abc:
        abc.delete()

    stat = model(
        user=user,
        data=dashboard_data[key]["data"],
        values=dashboard_data[key]["values"],
    )
    stat.save()


def update_plan(spreadsheet_id, sheet_id, sheet_title, request, row_num):
    print(f'update_plan: {update_plan}')
    orders_rub = request.pop("orders_rub")
    orders_count = request.pop("orders_count")
    sold_rub = request.pop("sold_rub")
    sold_count = request.pop("sold_count")
    logistic = request.pop("logistic")
    realize = request.pop("realize")
    sell_percent = request.pop("sell_percent")
    return insert_plan(spreadsheet_id, sheet_id, sheet_title,
                       (
                           orders_rub,
                           orders_count,
                           sold_rub,
                           sold_count,
                           logistic,
                           realize,
                           sell_percent
                       ), row_num
                       )


def get_object_plan(request):
    user = request.user
    user_id = user.pk

    spreadsheet = Spreadsheet.objects.filter(user_id=user_id, spreadsheet_title="Wildberries")
    if not spreadsheet:
        return None

    spreadsheet = spreadsheet.first()

    user_sheets = UserSheet.objects.filter(spreadsheet_id=spreadsheet.pk)

    if not user_sheets:
        return None
    user_sheet = None

    for sheet in user_sheets:
        if sheet.sheet_title.title == "План":
            user_sheet = sheet
    return user_sheet


def put_plan(get_object_func, response, request, status, row_num):
    model_object = get_object_func()
    spreadsheet_id = model_object.spreadsheet.spreadsheet_id
    sheet_id = model_object.sheet_id

    sheet_title = model_object.sheet_title.title
    for num in request.data.values():

        if not isinstance(num, int):
            return response(status=status.HTTP_400_BAD_REQUEST)

    if update_plan(spreadsheet_id, sheet_id, sheet_title, request.data, row_num):
        return response(status=status.HTTP_200_OK)
    return response(status=status.HTTP_400_BAD_REQUEST)


def get_queryset_dynamic_report_dashboard(report_class, request):
    user_id = request.user.pk

    report_class_instance = report_class.objects.filter(user_id=user_id)

    return report_class_instance


def get_object_dynamic_report_dashboard(report_class, request):
    user_id = request.user.pk

    report_class_instance = report_class.objects.filter(user_id=user_id)

    return report_class_instance.first()


def collect_self_sell_data(queryset, data):
    queryset = queryset.order_by("-total_amount")
    total_sum = 0
    total_amount = 0
    for instance in queryset:
        total_sum += instance.total_sum
        total_amount += instance.total_amount
    article = queryset[0].article
    article_total = queryset[0].total_amount

    data["total_sum"] = total_sum
    data["total_amount"] = total_amount
    data["article"] = article
    data["article_total"] = article_total
