import requests
import time

from config.constants import WB_TOKEN, DEFAULT_USER_AGENT, ATTEMPT_LIMIT, DEFAULT_TIMEOUT_VALUE, SELLER_HOST, \
    TIMEOUT_INCREMENTAL

PERSONAL_ACCOUNT_API_URL = 'https://seller.wildberries.ru/ns/weeklydynamics/analytics-back/api/v1'


class PersonalAccountAPI:
    @staticmethod
    def get_stocks(supplier_id, date_from, date_to, brand_id=0, contract_id=-100, office_id=-100, limit=100, offset=0):
        url = PERSONAL_ACCOUNT_API_URL + '/weekly-report-table-balance'
        balance = []
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1

        headers = {
            'Cookie': f"WBToken={WB_TOKEN}; x-supplier-id={supplier_id}",
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Host': SELLER_HOST,
            'Origin': 'https://seller.wildberries.ru',
            'Referer': 'https://seller.wildberries.ru/analytics/weekly-dynamics',
            'User-Agent': DEFAULT_USER_AGENT
        }
        body = {'brandID': brand_id, "contractID": contract_id, "officeID": office_id, "dateFrom": date_from,
                "dateTo": date_to}

        session = requests.Session()
        while True:
            try:
                params = {'limit': limit, 'offset': offset}
                response = session.request("POST", url=url, headers=headers, json=body, params=params, timeout=timeout)
                if response.status_code == 200 and response.json():
                    balance.append(response.json())
                    if len(response.json()) < 100:
                        break
                    offset += limit
                    continue
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return balance

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL
        return balance

    @staticmethod
    def get_dynamic(supplier_id, date_from, date_to, brand_id=0, contract_id=-100, office_id=-100, limit=100, offset=0):
        url = PERSONAL_ACCOUNT_API_URL + '/weekly-report-table'
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        dynamic = []
        headers = {
            'Cookie': f"WBToken={WB_TOKEN}; x-supplier-id={supplier_id}",
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Host': 'seller.wildberries.ru',
            'Origin': 'https://seller.wildberries.ru',
            'Referer': 'https://seller.wildberries.ru/analytics/weekly-dynamics',
            'User-Agent': DEFAULT_USER_AGENT
        }

        body = {'brandID': brand_id, "contractID": contract_id, "officeID": office_id, "dateFrom": date_from,
                "dateTo": date_to}
        session = requests.Session()

        while True:
            try:
                params = {'limit': limit, 'offset': offset}
                response = session.request("POST", url=url, headers=headers, json=body, params=params, timeout=timeout)
                if response.status_code == 200 and response.json():
                    dynamic.append(response.json())
                    if len(response.json()) < 100:
                        break
                    offset += limit
                    continue
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return dynamic

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL
        return dynamic

    @staticmethod
    def get_nomenclatures(supplier_id, limit=100, offset=0):
        nomenclatures = []
        url = 'https://seller.wildberries.ru/ns/nomenclatures/analytics-back/api/v1/nomenclatures'
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1

        headers = {
            'Cookie': f"WBToken={WB_TOKEN}; x-supplier-id={supplier_id}",
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Host': SELLER_HOST,
            'Origin': 'https://seller.wildberries.ru',
            'Referer': 'https://seller.wildberries.ru/analytics/nomenclatures',
            'User-Agent': DEFAULT_USER_AGENT
        }

        session = requests.Session()
        while True:
            try:
                params = {'limit': limit, 'offset': offset}
                response = session.request("GET", url=url, headers=headers, params=params, timeout=timeout)
                if response.status_code == 200 and response.json():
                    s = response.json()
                    s = s.get('data').get('nomenclatures')
                    nomenclatures.extend(s)
                    if len(s) < 100:
                        break

                    offset += limit
                    continue
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return nomenclatures

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL
        return nomenclatures

    @staticmethod
    def get_stocks_by_region(supplier_id, limit=100, offset=0):
        stocks = []
        url = "https://seller.wildberries.ru/ns/balances/analytics-back/api/v1/balances"
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1

        headers = {
            'Cookie': f"WBToken={WB_TOKEN}; x-supplier-id={supplier_id}",
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Host': SELLER_HOST,
            'Origin': 'https://seller.wildberries.ru',
            'Referer': 'https://seller.wildberries.ru/analytics/warehouse-remains',
            'User-Agent': DEFAULT_USER_AGENT
        }

        body = {"filters": ["brand", "subject", "supplierArticle", "nmId",
                            "techSize", "quantityInTransit",
                            "quantityForSaleTotal"]}

        session = requests.Session()
        while True:
            try:
                params = {'limit': limit, 'offset': offset}
                response = session.request("POST", url, headers=headers, json=body, params=params, timeout=timeout)
                if response.status_code == 200 and response.json():
                    data = response.json()
                    data = data.get('data').get('balances')

                    stocks.append(response.json())
                    if len(data) < limit:
                        break
                    offset += limit
                    continue
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return stocks

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL
        return stocks

    @staticmethod
    def get_consolidated_table(wb_token, supplier_id):
        url = 'https://seller.wildberries.ru/ns/consolidated/analytics-back/api/v1/consolidated-table'
        params = {'isCommussion': 2}
        attempt, timeout = 1, DEFAULT_TIMEOUT_VALUE

        headers = {
            'Cookie': f"WBToken={wb_token}; x-supplier-id={supplier_id}",
            'Content-type': 'application/json',
            'Accept': '*/*',
            'User-Agent': DEFAULT_USER_AGENT
        }

        session = requests.Session()
        while True:
            try:
                response = session.get(url, params=params, headers=headers, timeout=timeout)
                if not response.json():
                    print("Нет данных")
                    return None

                if response.status_code == 200:
                    print("Готово")
                    return response.json()

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    @staticmethod
    def get_feedbacks(wb_token, supplier_id):
        url = 'https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks'
        headers = {'Cookie': f"WBToken={wb_token}; x-supplier-id={supplier_id}",
                   'Content-type': 'application/json',
                   'Accept': '*/*',
                   'Host': SELLER_HOST,
                   'Origin': 'https://seller.wildberries.ru',
                   'Referer': 'https://seller.wildberries.ru/feedback-question/feedbacks/not-answered-feedbacks',
                   'User-Agent': DEFAULT_USER_AGENT
                   }
        skip, take = 0, 5000
        params = {"metaDataKeyMustNot": "norating",
                  "nmId": "",
                  "order": "dateDesc",
                  }
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        feedbacks = []
        is_answered_vars = ("false", "true")
        session = requests.Session()
        for is_answered in is_answered_vars:
            params["isAnswered"] = is_answered
            skip = 0
            while True:
                try:
                    params["skip"] = skip
                    params["take"] = take
                    response = session.request("GET", url, headers=headers, params=params, timeout=timeout)
                    if response.status_code == 200 and response.json():
                        data = response.json().get('data')
                        feedbacks.extend(data.get('feedbacks'))

                        response_length = len(data.get('feedbacks'))
                        if response_length < take:
                            count_archive = data.get('countArchive')
                            count_unanswered = data.get('countUnanswered')
                            break
                        skip += take
                        continue
                    if attempt == ATTEMPT_LIMIT:
                        print("Превышен лимит ожидания")
                        return feedbacks

                    attempt += 1
                except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                    session.close()
                    session = requests.Session()
                    attempt += 1
                    timeout += TIMEOUT_INCREMENTAL
        return feedbacks

    @staticmethod
    def get_finance_reports_id(wb_token, supplier_id, offset=0, limit=100):
        url = 'https://seller.wildberries.ru/ns/realization-reports/suppliers-portal-analytics/api/v1/reports?type=2'
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        dynamic = []
        headers = {
            'Cookie': f"WBToken={wb_token}; x-supplier-id={supplier_id}",
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Host': 'seller.wildberries.ru',
            'Origin': 'https://seller.wildberries.ru',
            'Referer': 'https://seller.wildberries.ru/suppliers-mutual-settlements/reports-implementations/reports-weekly',
            'User-Agent': DEFAULT_USER_AGENT
        }
        #
        body = {}
        session = requests.Session()

        while True:
            try:
                response = session.request("GET", url=url, headers=headers, json=body, timeout=timeout)
                if response.status_code == 200 and response.json():
                    dynamic.append(response.json())
                    if len(response.json()) < 100:
                        break
                    offset += limit
                    continue
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return dynamic

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL
        return dynamic

    @staticmethod
    def get_weekly_finance_report(wb_token, supplier_id, report_id, offset=0, limit=100):
        url = f'https://seller.wildberries.ru/ns/realization-reports/suppliers-portal-analytics/' \
              f'api/v1/reports/{report_id}/details'
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        dynamic = []
        headers = {
            'Cookie': f"WBToken={wb_token}; x-supplier-id={supplier_id}",
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Host': 'seller.wildberries.ru',
            'Origin': 'https://seller.wildberries.ru',
            'Referer': f'https://seller.wildberries.ru/suppliers-mutual-settlements/'
                       f'reports-implementations/reports-weekly/{report_id}',
            'User-Agent': DEFAULT_USER_AGENT
        }
        #
        body = {}
        session = requests.Session()

        while True:
            try:
                response = session.request("GET", url=url, headers=headers, json=body, timeout=timeout)
                if response.status_code == 200 and response.json():
                    dynamic.append(response.json())
                    if len(response.json()) < 100:
                        break
                    offset += limit
                    continue
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return dynamic

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL
        return dynamic

    @staticmethod
    def get_sales_id(supplier_id, date_from, date_to):
        url = 'https://seller.wildberries.ru/ns/reportsviewer/analytics-back/api/report/supplier-goods/order'
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        headers = {
            'Cookie': f"WBToken={WB_TOKEN}; x-supplier-id={supplier_id}",
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Host': 'seller.wildberries.ru',
            'Origin': 'https://seller.wildberries.ru',
            'Referer': 'https://seller.wildberries.ru/analytics/sales',
            'User-Agent': DEFAULT_USER_AGENT
        }
        params = {"dateFrom": date_from, "dateTo": date_to}
        session = requests.Session()
        while True:
            try:
                response = session.request("POST", url=url, headers=headers, params=params,
                                           timeout=timeout)
                if response.status_code == 200 and response.json():
                    id = response.json().get('data').get('id')
                    return id
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    @staticmethod
    def get_sales(supplier_id, id, limit=100, offset=0, direction='ASC'):
        time.sleep(20)
        group_columns_name = []
        url = 'https://seller.wildberries.ru/ns/reportsviewer/analytics-back/api/report/supplier-goods/data/' + id
        headers = {'Cookie': f"WBToken={WB_TOKEN}; x-supplier-id={supplier_id}",
                   'Content-type': 'application/json',
                   'Accept': '*/*',
                   'Host': SELLER_HOST,
                   'Referer': 'https://seller.wildberries.ru/analytics/sales/' + id,
                   'User-Agent': DEFAULT_USER_AGENT
                   }
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        session = requests.Session()
        while True:
            try:
                params = {'direction': direction, 'limit': limit, 'offset': offset, 'sort': ''}
                response = session.request("GET", url, headers=headers, params=params, timeout=timeout)
                if response.status_code == 200 and response.json():
                    data_json = response.json().get('data')
                    data = data_json.get('data')
                    group_columns_name.append(data)
                    response_length = len(data)
                    offset += response_length
                    if response_length < limit:
                        break
                    continue
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return
                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL
        return group_columns_name

    def get_wb_token(self, wild_auth_token):
        url = 'https://seller.wildberries.ru/passport/api/v2/auth/wild_v3_upgrade'
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        headers = {
            'Cookie': f"WILDAUTHNEW_V3={wild_auth_token}",
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Host': 'seller.wildberries.ru',
            'Origin': 'https://seller.wildberries.ru',
            'User-Agent': DEFAULT_USER_AGENT
        }

        body = {"device": "Windows"}
        session = requests.Session()

        while True:
            try:
                response = session.request("POST", url=url, headers=headers, json=body, timeout=timeout)
                if response.status_code == 200 and response.json():
                    return response.cookies.values()
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return
                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    def get_supplier_id(self, wb_token):
        url = 'https://seller.wildberries.ru/ns/suppliers/suppliers-portal-eu/suppliers/getUserSuppliers'
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        headers = {
            'Cookie': f"WBToken={wb_token}",
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Host': 'seller.wildberries.ru',
            'Origin': 'https://seller.wildberries.ru',
            'User-Agent': DEFAULT_USER_AGENT
        }

        body = [{"method": "getUserSuppliers", "params": {}, "id": "json-rpc_3", "jsonrpc": "2.0"}, {
            "method": "listCountries", "params": {}, "id": "json-rpc_4", "jsonrpc": "2.0"}]
        session = requests.Session()
        supplier_id_list = []

        while True:
            try:
                response = session.request("POST", url=url, headers=headers, json=body, timeout=timeout)
                if response.status_code == 200 and response.json():
                    supplier_id_list.append(response.json()[0]["result"])
                    return supplier_id_list
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    @staticmethod
    def get_position(search_query, nomenclature):
        url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        headers = {
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Host': 'search.wb.ru',
            'Origin': 'https://www.wildberries.ru/',
            'Referer': 'https://www.wildberries.ru/',
            'User-Agent': DEFAULT_USER_AGENT
        }

        body = {"appType": "1",
                "couponsGeo": "12,3,18,15,21",
                "curr": "rub",
                "dest": "-1075831,-115100,-382776,-2361092",
                "emp": "0",
                "lang": "ru",
                "locale": "ru",
                "pricemarginCoeff": "1.0",
                "query": search_query,
                "reg": "1",
                "regions": "68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,40,1,48,71",
                "resultset": "catalog",
                "sort": "popular",
                "spp": "21",
                "suppressSpellcheck": "false",
                }
        session = requests.Session()
        page = 1

        while True:
            try:
                body["page"] = page
                response = session.request("GET", url=url, headers=headers, params=body, timeout=timeout)
                if response.status_code == 200 and response.json():

                    subjects = response.json().get("data").get("products")
                    for position, subject in enumerate(subjects):
                        if subject.get("id") == int(nomenclature):
                            subject_position = position + 1
                            if page > 1:
                                subject_position += page * 100
                            return subject_position
                    page += 1
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL


if __name__ == '__main__':
    wb = 'Ava4vBfW7amuDNapk68MQk9-R3v9T-MscrW2Fj8OEAjFlnoocCzF6Ql-cRSaHESSSPcHbBBg7Ub9WQJ6WaEbAQl6Kzib4W2y89oVCqEIKyXG8A'
    s_l = PersonalAccountAPI().get_position("рубашка женская", "75548184")
    print(s_l)
