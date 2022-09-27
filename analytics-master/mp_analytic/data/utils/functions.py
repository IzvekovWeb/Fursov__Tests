import datetime

from pytz import timezone


def html_color_to_json(html_color):
    if html_color.startswith("#"):
        html_color = html_color[1:]
    return {"red": int(html_color[0:2], 16) / 255.0, "green": int(html_color[2:4], 16) / 255.0,
            "blue": int(html_color[4:6], 16) / 255.0}


def form_days_start_date(days_count: int, flag_today: int = 1, dot_format: int = 0,
                         date_format="%Y-%m-%d", start_date=None):
    if start_date is None:
        start_date = datetime.date.today()
    else:
        start_date = start_date[:6] + '20' + start_date[6:]
        start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y")

    days = []
    if days_count == 0:
        days_count = 7

    for i in range(flag_today, days_count + 1):
        if dot_format:
            days.append(date_to_point_format((start_date - datetime.timedelta(i)).strftime(date_format)))
        else:
            days.append((start_date - datetime.timedelta(i)).strftime(date_format))
    days.reverse()
    return days


def form_days(days_count: int, flag_today: int = 1, dot_format: int = 0,
              date_format="%Y-%m-%d"):  # If flag_today == 0 => days include today

    start_date = datetime.date.today()
    days = []

    if days_count == 0:
        days_count = 7

    for i in range(flag_today, days_count + 1):
        if dot_format:
            days.append(date_to_point_format((start_date - datetime.timedelta(i)).strftime(date_format)))
        else:
            days.append((start_date - datetime.timedelta(i)).strftime(date_format))
    days.reverse()
    return days


def form_period_days(start_day, end_day) -> list:
    start_date = datetime.datetime.strptime(start_day, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_day, "%Y-%m-%d")
    today = datetime.datetime.today()
    if not today >= end_date >= start_date:
        raise Exception
    delta = end_date - start_date
    delta = delta.days

    period = []
    for i in range(delta + 1):
        period.append((start_date + datetime.timedelta(i)).strftime("%Y-%m-%d"))
    return period


def form_days_mpstats(days_count: int):
    """
    param days_count: The count of days
    :return: List of datetime
    """
    today = datetime.date.today()
    days = []
    days_count = [1, days_count]
    for i in days_count:
        days.append((today - datetime.timedelta(i)).strftime("%Y-%m-%d"))
    days.reverse()
    return tuple(days)


def form_dates_percents(date_from, date_to):
    start_date = datetime.datetime.strptime(date_from, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(date_to, "%Y-%m-%d")
    today = datetime.datetime.today()
    if not today >= end_date >= start_date:
        raise Exception
    return start_date, end_date


def form_date_feedbacks(date: str) -> str:
    date = datetime.datetime.strptime(date[:16], "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M")
    return date


def compare_dates(date_first: str, date_sec):
    date_first = datetime.datetime.strptime(date_first, "%Y-%m-%d %H:%M")
    date_sec = datetime.datetime.strptime(date_sec, "%Y-%m-%d %H:%M")
    return date_first > date_sec


def update_at(response, table_insert=None, sheet_name=None):
    obj_update_at = datetime.datetime.now(timezone("Europe/Moscow"))
    offset = 2
    start_column = chr(len(response[0]) + offset + 65)  # 65 - ASCII -> "A"

    if table_insert:
        table_insert(
            [[f'Обновлено: {obj_update_at.strftime("%d.%m.%Y %H:%M")}']],
            start_column=start_column,
            sheet_name=sheet_name
        )
    return obj_update_at


def percent(total, _percent):
    return round(int(total) - (int(total) / 100 * int(_percent)))


def lug_rub_(plan, fact):
    return tuple([plan[i] - fact[i] for i in range(len(plan))])


def div_length_(fact, length):
    return tuple([i / length for i in fact])


def div_(x, y):
    return tuple([0 if y[i] == 0 else x[i] / y[i] for i in range(len(x))])


def div_percent_(x, y):
    return tuple([0 if y[i] == 0 else x[i] / y[i] for i in range(len(x))])


def dynamic(last, pre_last):
    result = []

    for i in range(len(last)):
        result.append((last[i] - pre_last[i]) / pre_last[i]) if pre_last[i] != 0 else result.append(1)

    return tuple(result)


def get_data_from_consolidated_table(data: dict, year, month, day):
    for cons_years in data['data']['consolidatedYears']:
        if cons_years['year'] == year:
            for cons_months in cons_years['consolidatedMonths']:
                if month == cons_months['month']:
                    for day_data in cons_months['consolidatedDays']:
                        if day_data['day'] == day:
                            return day_data
    return None


def normalize_hour(hour):
    start_hour = f'00:00'
    end_hour = f'{hour + 1}:00'
    if hour == 23:
        end_hour = f'{hour}:59'
    start_time = datetime.datetime.strptime(start_hour, '%H:%M').strftime("%H:%M")
    end_time = datetime.datetime.strptime(end_hour, '%H:%M').strftime("%H:%M")
    return f'{start_time}-{end_time}'


def normalize_price(price):
    return round((price / 85) * 100, 1)


def date_to_point_format(date):
    return f"{date[8:]}.{date[5:7]}.{date[2:4]}"

