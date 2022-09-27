import datetime

import requests

from config.constants import WB_API_SUPPLIER_URL, WB_TOKEN, WB_API_SUPPLIER_STATS_URL, MP_STATS, DEFAULT_TIMEOUT_VALUE
from config.suppliers import SUPPLIERS
from data.utils.functions import form_days_mpstats


# TODO refactor all dicts
class OrdersStatisticsWB(object):
    def __init__(self):
        pass

    @staticmethod
    def get_cards(supplier):
        """
        :param supplier: Supplier
        :return: Response with part numbers
        """
        url = WB_API_SUPPLIER_URL + "/card/list"

        headers = {
            "Host": 'suppliers-api.wildberries.ru',
            "Content-Type": "application/json",
            "Authorization": supplier.get('token'),
        }

        body = {
            "id": 1,
            "jsonrpc": "2.0",
            "params": {
                "isArchive": True,
                "query": {
                    "limit": 10000,
                    "offset": 0,
                    "total": 0
                },
                "withError": False
            }
        }

        timeout = 40
        session = requests.Session()

        if not supplier.get('old'):
            return None

        name = supplier.get("name")
        print(f"Сбор номенклатур для поставщика {name}")

        body['params']['supplierID'] = supplier.get('supplier-id')
        while True:
            try:
                response = session.post(url=url, headers=headers, json=body, timeout=timeout)
                if response.status_code == 200:
                    break
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                timeout += 5
        return response

    @staticmethod
    def get_card_list_order_by_count_article():
        """
        :return: Response with card list
        """
        response_result = {}

        for supplier in SUPPLIERS.values():  # бежим по поставщикам
            response = OrdersStatisticsWB().get_cards(supplier)
            if not response:
                continue

            # Карточки запроса
            cards = response.json()['result']['cards']
            for cards_item in cards:
                brand = ''  # Название бренда
                for addin in cards_item['addin']:
                    if addin['type'] == "Бренд":
                        # если в addin карточки был параметр Бренд - запишем его
                        brand = addin['params'][0]['value']

                for nomenclature in cards_item['nomenclatures']:
                    article = cards_item['supplierVendorCode'][:-1]
                    category = cards_item['parent'] + '/' + cards_item['object']
                    if response_result.get(article):
                        continue

                    response_result[article] = {
                        'supplier': supplier.get('name'),
                        'nmId': nomenclature['nmId'],
                        'article': article,
                        'category': category,
                        'brand': brand
                    }
        return response_result

    @staticmethod
    def get_card_list_order_by_count():
        """
        :return: Response with card list
        """
        response_result = {}

        for supplier in SUPPLIERS.values():  # бежим по поставщикам
            response = OrdersStatisticsWB().get_cards(supplier)
            if not response:
                continue

            # Карточки запроса
            cards = response.json()['result']['cards']
            for cards_item in cards:
                brand = ''  # Название бренда
                for addin in cards_item['addin']:
                    if addin['type'] == "Бренд":
                        # если в addin карточки был параметр Бренд - запишем его
                        brand = addin['params'][0]['value']

                for nomenclature in cards_item['nomenclatures']:
                    article = cards_item['supplierVendorCode'] + nomenclature['vendorCode']
                    category = cards_item['parent'] + '/' + cards_item['object']
                    response_result[nomenclature['nmId']] = {
                        'supplier': supplier.get('name'),
                        'nmId': nomenclature['nmId'],
                        'article': article,
                        'category': category,
                        'brand': brand
                    }

        return response_result

    @staticmethod
    def get_card_list_feedback():
        """
        :return: Response with card list in feedbacks
        """
        response_result = {}

        nomen_articul_dict = {}
        cards_dict = {}

        for supplier in SUPPLIERS.values():  # бежим по поставщикам
            response = OrdersStatisticsWB().get_cards(supplier)
            if not response:
                continue

            name = supplier.get("name")
            if not cards_dict.get(name):
                cards = response.json()['result']['cards']

                for card in cards:
                    if not nomen_articul_dict.get('supplierVendorCode'):
                        nomen_articul_dict['supplierVendorCode'] = {}
                    nomen_articul_dict['supplierVendorCode'][card['supplierVendorCode']] = {'nmId': [],
                                                                                            'imtId': card['imtId']}
                    for nomen in card['nomenclatures']:
                        nomen_articul_dict['supplierVendorCode'][card['supplierVendorCode']]['nmId'].append(
                            nomen['nmId'])

            for vendor in nomen_articul_dict['supplierVendorCode'].values():
                if not response_result.get(name):
                    response_result[name] = {'imtId': []}
                response_result[name]['imtId'].append(vendor['imtId'])
        return response_result

    @staticmethod
    def get_orders(token, key, day, name):
        url = WB_API_SUPPLIER_STATS_URL + '/orders'
        """
        :param token: Токен авторизации
        :param name: Имя поставщика
        :param key: Токен авторизации x64
        :param day: День поставки
        :param url: Ссылка
        """

        headers = {'Authorization': token, 'User-Agent': 'Mozilla/5.0'}  # Параметры заголовков
        params = {'dateFrom': day, 'key': key, 'flag': 1}  # Параметры запроса
        timeout = 40
        session = requests.Session()
        attempt = 1

        while True:
            try:
                print(f"\rОбрабатываем - {name}{(' ' * (20 - len(name)))} Попытка: \t{attempt}", end="  ")
                response = session.get(url=url, headers=headers, params=params, timeout=timeout)
                if response.status_code == 200:
                    print("Готово")
                    return response.json()
                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                timeout += 10
                session = requests.Session()

    @staticmethod
    def get_data(name):
        url = 'https://seller.wildberries.ru/ns/consolidated/analytics-back/api/v1/consolidated-table'
        params = {'isCommussion': 2}
        session = requests.Session()
        attempt = 1
        timeout = 40
        headers = {
            'Cookie': f"WBToken={WB_TOKEN};x-supplier-id={SUPPLIERS[name]['supplier-id']}"}
        while True:
            try:
                print(f"\rОбрабатываем - {name}{(' ' * (20 - len(name)))} Попытка: \t{attempt}", end="  ")
                response = session.get(url=url, params=params, headers=headers, timeout=timeout)
                if response.status_code == 200:
                    print("Готово")
                    return response.json()
                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                timeout += 10
                session = requests.Session()

    @staticmethod
    def get_stocks(token, key, name, timedelta=0):
        url = WB_API_SUPPLIER_STATS_URL + "/stocks"

        headers = {"Authorization": token}
        session = requests.Session()

        attempt = 1
        timeout = 40
        while True:
            try:
                print(f"\rОбрабатываем - {name}{(' ' * (20 - len(name)))} Попытка: \t{attempt}", end="  ")
                date = datetime.date.today() - datetime.timedelta(timedelta)
                params = {'dateFrom': date.strftime("%Y-%m-%d"), "key": key}
                response = session.get(url=url, headers=headers, params=params, timeout=timeout)
                if response.status_code == 200:
                    if not response.json():
                        timedelta += 1
                        continue
                    print("Готово")
                    return response.json()

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                timeout += 5
                session = requests.Session()

    @staticmethod
    def mapping_dict_to_list(response_dict, days_list) -> list:
        """
        :return: Список из кортежей данных
        """

        table = [("Поставщик", "Номенклатура", "Артикул", "Категория", *days_list,
                  "Итого"), ]  # Создаем список, первый элемент - кортеж заголовков

        values = response_dict.values()  # Получаем данные из словаря

        for value in values:
            each_day = []
            orders_count = 0  # Переменная для подсчета общего количества
            for day in days_list:
                if day in value.keys():
                    each_day.append(value[day])
                    orders_count += value[day]
                else:
                    each_day.append(0)
            each_day.append(orders_count)
            row = (value['supplier'], value['nmId'], value['article'], value['category'],
                   *each_day)  # Формирование кортежа данных
            table.append(row)
        return table

    @staticmethod
    def report_detail_by_period(supplier, dates):
        if not supplier.get('old'):
            return None

        url = WB_API_SUPPLIER_STATS_URL + '/reportDetailByPeriod'

        headers = {
            "Content-Type": "application/json",
            "Authorization": supplier.get('token'),
        }

        timeout = 40
        session = requests.Session()
        name = supplier.get("name")
        limit = 100000

        url += f'?dateFrom={dates[0]}' \
               f'&key={supplier.get("x64key")}' \
               f'&limit={limit}' \
               f'&dateTo={dates[1]}'

        print(f"Сбор номенклатур для поставщика {name}")

        while True:
            try:
                response = session.get(url=url, headers=headers, timeout=timeout)
                if response.status_code == 200:
                    break
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                timeout += 5
        return response.json()

    @staticmethod
    def get_mpstats_response(nm_list: list, category: str = None):
        date_from, date_to = form_days_mpstats(7)
        url = f'https://mpstats.io/api/wb/get'

        session = requests.Session()
        headers = {'X-Mpstats-TOKEN': MP_STATS,
                   'User-Agent': 'Mozilla/5.0',
                   "Content-Type": "application/json"}
        params = {
            'd1': date_from,
            'd2': date_to
        }
        timeout = DEFAULT_TIMEOUT_VALUE
        dict_list = []
        filter_model = 'id'
        filter_type = 'number'

        if category:
            filter_model = 'seller'
            filter_type = 'text'
            params['path'] = category

        for nm in nm_list:
            while True:
                try:
                    body = {
                        "filterModel":
                            {
                                filter_model:
                                    {
                                        "filterType": filter_type,
                                        "type": "equals",
                                        "filter": nm
                                    }
                            }
                    }
                    response = session.request(
                        method=get_mp_stats_method(nm),
                        url=url + get_mp_stats_url(nm),
                        headers=headers,
                        params=params,
                        timeout=timeout,
                        json=body
                    )
                    if response.status_code == 200:
                        if category:
                            dict_list.append(response.json())
                            print(f"Готово: {nm}")
                        else:
                            dict_list.append(
                                {nm: response.json()}
                            )
                        break
                    elif response.status_code == 500:
                        dict_list.append(nm)
                        print(f'По номенклатуре № {nm} - нет данных!')
                        break

                except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                    session.close()
                    session = requests.Session()
                    timeout += 5
        return dict_list

    @staticmethod
    def get_mpstats_response_max_categories(category: str = None):
        date_from, date_to = form_days_mpstats(7)
        url = f'https://mpstats.io/api/wb/get'

        session = requests.Session()
        headers = {'X-Mpstats-TOKEN': MP_STATS,
                   'User-Agent': 'Mozilla/5.0',
                   "Content-Type": "application/json"}
        params = {
            'd1': date_from,
            'd2': date_to
        }
        timeout = DEFAULT_TIMEOUT_VALUE
        dict_list = []

        filter_model = 'category_position'
        filter_type = 'number'
        params['path'] = category

        while True:
            try:
                body = {
                    "filterModel":
                        {
                            filter_model:
                                {
                                    "filterType": filter_type,
                                    "type": "lessThan",
                                    "filter": 101
                                }
                        }
                }
                response = session.request(
                    method='POST',
                    url=url + "/category",
                    headers=headers,
                    params=params,
                    timeout=timeout,
                    json=body
                )
                if response.status_code == 200:
                    dict_list.append(response.json())
                    print(f'Получены данные по категории {category}')
                    break

                elif response.status_code == 500:
                    dict_list.append(category)
                    print(f'Нет данных! По категории {category}')
                    break

            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                timeout += 5
        return dict_list

    @staticmethod
    def get_dynamic_prices_mp_stats(nm_ids):
        date_from, date_to = form_days_mpstats(3)
        timeout = DEFAULT_TIMEOUT_VALUE
        dict_list = []

        session = requests.Session()
        headers = {'X-Mpstats-TOKEN': MP_STATS,
                   'User-Agent': 'Mozilla/5.0',
                   "Content-Type": "application/json"}

        params = {'d1': date_from,
                  'd2': date_to}

        for nm_id in nm_ids:
            while True:
                try:
                    url = f"https://mpstats.io/api/wb/get/item/{nm_id}/sales"
                    response = session.request(method='GET',
                                               url=url,
                                               headers=headers,
                                               params=params,
                                               timeout=timeout)
                    if response.status_code == 200:
                        dict_list.append(response.json())
                        break
                except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                    session.close()
                    session = requests.Session()
                    timeout += 5
        return dict_list


def get_mp_stats_url(nm):
    if isinstance(nm, str):
        return '/category'
    else:
        return f'/item/{nm}/by_category'


def get_mp_stats_method(nm):
    if isinstance(nm, str):
        return 'POST'
    else:
        return 'GET'
