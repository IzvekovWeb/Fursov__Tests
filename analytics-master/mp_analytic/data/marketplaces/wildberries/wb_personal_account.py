import requests

from config.constants import \
    DEFAULT_USER_AGENT, \
    ATTEMPT_LIMIT, \
    DEFAULT_TIMEOUT_VALUE, \
    TIMEOUT_INCREMENTAL, \
    WB_PERSONAL_ACCOUNT_API_URL, \
    HEADERS_PERSONAL_ACCOUNT_API


class PersonalAccountAPI:
    @staticmethod
    def get_request(session, method, url, headers, timeout, params=None, body=None):
        if body:
            request = session.request(method=method,
                                      url=url,
                                      headers=headers,
                                      json=body,
                                      params=params,
                                      timeout=timeout)
        elif params and not body:
            request = session.request(method=method,
                                      url=url,
                                      headers=headers,
                                      params=params,
                                      timeout=timeout)
        else:
            request = session.request(method=method,
                                      url=url,
                                      headers=headers,
                                      timeout=timeout)
        return request

    @staticmethod
    def session_request(method, url, headers, body=None, keyword=None, params_flag=True,
                        limit=100, offset=0):
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        session = requests.Session()
        result = []

        while True:
            try:
                if params_flag:
                    params = {'limit': limit, 'offset': offset}
                    response = PersonalAccountAPI.get_request(session, method, url, headers, timeout, params, body)
                else:
                    response = PersonalAccountAPI.get_request(session, method, url, headers, timeout, body=body)

                if response.status_code == 200 and response.json():
                    response_json = response.json()
                    if isinstance(response_json, dict) and response_json.get("error"):
                        return

                    if keyword:
                        response_json = response_json.get("data").get(keyword)
                    result.append(response_json)
                    if len(response_json) < limit and params_flag:
                        return result
                    elif not params_flag:
                        return result

                    offset += limit
                    continue

                elif response.status_code == 401:
                    print(401)
                    raise PermissionError

                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return result

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    @staticmethod
    def get_dynamic_stocks(supplier_id, wb_token, date_from, date_to,
                           url, brand_id, contract_id, office_id):
        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}; x-supplier-id={supplier_id}"
        headers["Referer"] = WB_PERSONAL_ACCOUNT_API_URL + "/analytics/weekly-dynamics"

        body = {
            "brandID": brand_id,
            "contractID": contract_id,
            "officeID": office_id,
            "dateFrom": date_from,
            "dateTo": date_to
        }

        return PersonalAccountAPI.session_request("POST", url, headers, body)

    @staticmethod
    def get_stocks(supplier_id, wb_token, date_from, date_to,
                   brand_id=0, contract_id=-100, office_id=-100):
        url = WB_PERSONAL_ACCOUNT_API_URL + "/ns/weeklydynamics/analytics-back/api/v1/weekly-report-table-balance"

        return PersonalAccountAPI.get_dynamic_stocks(supplier_id, wb_token, date_from, date_to, url,
                                                     brand_id, contract_id, office_id)

    @staticmethod
    def get_dynamic(supplier_id, wb_token, date_from, date_to,
                    brand_id=0, contract_id=-100, office_id=-100):
        url = WB_PERSONAL_ACCOUNT_API_URL + "/ns/weeklydynamics/analytics-back/api/v1/weekly-report-table"

        return PersonalAccountAPI.get_dynamic_stocks(supplier_id, wb_token, date_from, date_to, url,
                                                     brand_id, contract_id, office_id)

    @staticmethod
    def get_nomenclatures(supplier_id, wb_token):
        url = WB_PERSONAL_ACCOUNT_API_URL + "/ns/nomenclatures/analytics-back/api/v1/nomenclatures"

        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}; x-supplier-id={supplier_id}"
        headers["Referer"] = WB_PERSONAL_ACCOUNT_API_URL + "/analytics/nomenclatures"

        nomenclatures = PersonalAccountAPI.session_request("GET", url, headers, keyword="nomenclatures")
        nomenclatures_list = []
        for nomenclature in nomenclatures:
            nomenclatures_list.extend(nomenclature)
        return nomenclatures_list

    @staticmethod
    def get_stocks_by_region(supplier_id, wb_token):
        url = WB_PERSONAL_ACCOUNT_API_URL + "/ns/balances/analytics-back/api/v1/balances"

        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}; x-supplier-id={supplier_id}"
        headers["Referer"] = WB_PERSONAL_ACCOUNT_API_URL + "/analytics/warehouse-remains"

        body = {
            "filters": [
                "brand",
                "subject",
                "supplierArticle",
                "nmId",
                "techSize",
                "quantityInTransit",
                "quantityForSaleTotal"
            ]}

        stocks = PersonalAccountAPI.session_request("POST", url, headers, body=body, keyword="balances")
        return stocks

    @staticmethod
    def get_consolidated_table(wb_token, supplier_id):
        url = WB_PERSONAL_ACCOUNT_API_URL + "/ns/consolidated/analytics-back/api/v1/consolidated-table"

        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}; x-supplier-id={supplier_id}"
        if headers.get("Host"):
            headers.pop("Host")
        if headers.get("Origin"):
            headers.pop("Origin")

        session = requests.Session()
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        params = {'isCommussion': 2}
        while True:
            try:
                response = session.request("GET",
                                           url=url,
                                           params=params,
                                           headers=headers,
                                           timeout=timeout)
                if response.status_code == 200:
                    print("Готово")
                    return response.json()

                elif response.status_code == 401:
                    print(401)
                    raise PermissionError

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    @staticmethod
    def get_feedbacks(wb_token, supplier_id):
        url = WB_PERSONAL_ACCOUNT_API_URL + "/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks"

        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}; x-supplier-id={supplier_id}"
        headers["Referer"] = WB_PERSONAL_ACCOUNT_API_URL + "/feedback-question/feedbacks/not-answered-feedbacks"

        session = requests.Session()
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        skip, take = 0, 5000
        params = {
            "metaDataKeyMustNot": "norating",
            "nmId": "",
            "order": "dateDesc",
        }
        feedbacks = []
        is_answered_vars = ("false",)
        for is_answered in is_answered_vars:
            params["isAnswered"] = is_answered
            skip = 0
            while True:
                try:
                    params["skip"] = skip
                    params["take"] = take
                    response = session.request("GET",
                                               url=url,
                                               headers=headers,
                                               params=params,
                                               timeout=timeout)
                    if response.status_code == 200 and response.json():
                        data = response.json().get('data')
                        feedbacks.extend(data.get('feedbacks'))

                        response_length = len(data.get('feedbacks'))
                        if response_length < take:
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
    def get_finance_reports_id(wb_token, supplier_id):
        url = WB_PERSONAL_ACCOUNT_API_URL + "/ns/realization-reports/" \
                                            "suppliers-portal-analytics/api/v1/reports?type=2"

        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}; x-supplier-id={supplier_id}"
        headers["Referer"] = WB_PERSONAL_ACCOUNT_API_URL + "/suppliers-mutual-settlements/" \
                                                           "reports-implementations/reports-weekly"

        body = {}
        return PersonalAccountAPI.session_request("GET", url, headers, body=body, params_flag=False)

    @staticmethod
    def get_weekly_finance_report_count(wb_token, supplier_id, report_id):
        url = WB_PERSONAL_ACCOUNT_API_URL + f"/ns/realization-reports/suppliers-portal-analytics" \
                                            f"/api/v1/reports/{report_id}/details"
        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}; x-supplier-id={supplier_id}"
        headers["Referer"] = WB_PERSONAL_ACCOUNT_API_URL + f"https://seller.wildberries.ru/" \
                                                           f"suppliers-mutual-settlements/" \
                                                           f"reports-implementations/" \
                                                           f"reports-weekly/report/{report_id}"
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        params = dict(limit=0, skip=0)
        body = {}
        result = 0
        session = requests.Session()
        while True:
            try:
                response = PersonalAccountAPI.get_request(session, "GET", url=url, headers=headers,
                                                          params=params, body=body, timeout=timeout)
                if response.status_code == 200 and response.json():
                    result = response.json().get('data').get('count')
                    return result

                elif response.status_code == 401:
                    print(401)
                    raise PermissionError

                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return result

                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    @staticmethod
    def get_weekly_finance_report(wb_token, supplier_id, report_id):
        count = PersonalAccountAPI.get_weekly_finance_report_count(wb_token, supplier_id, report_id)

        url = WB_PERSONAL_ACCOUNT_API_URL + f"/ns/realization-reports/suppliers-portal-analytics/" \
                                            f"api/v1/reports/{report_id}/details"

        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}; x-supplier-id={supplier_id}"
        headers["Referer"] = WB_PERSONAL_ACCOUNT_API_URL + f"/suppliers-mutual-settlements/" \
                                                           f"reports-implementations/reports-weekly/{report_id}"

        body = {}
        dynamic = []
        limit = count if count <= 2500 else 2500
        offset = 0
        session = requests.Session()
        timeout, attempt = 150, 1

        while True:
            try:
                params = dict(limit=limit, skip=offset)
                response = PersonalAccountAPI.get_request(session, "GET", url=url, headers=headers,
                                                          params=params, body=body, timeout=timeout)
                if response.status_code == 200 and response.json():
                    dynamic.extend(response.json().get('data').get('details'))
                    if len(dynamic) == count:
                        return dynamic

                    offset = len(dynamic)

                elif response.status_code == 401:
                    print(401)
                    raise PermissionError

                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return dynamic

                if attempt == 500 and not len(dynamic):
                    print("Break Finance Report")
                    raise ConnectionError
              
                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    @staticmethod
    def get_wb_token(wild_auth_token):
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
                    cookies = response.cookies.get("WBToken")
                    return cookies
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return
                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    @staticmethod
    def get_supplier_id(wb_token):
        url = WB_PERSONAL_ACCOUNT_API_URL + "/ns/suppliers/suppliers-portal-core/suppliers"

        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}"

        body = [
            {
                "method": "getUserSuppliers",
                "params": {},
                "id": "json-rpc_3",
                "jsonrpc": "2.0"
            },
            {
                "method": "listCountries",
                "params": {},
                "id": "json-rpc_4",
                "jsonrpc": "2.0"}]

        supplier_id_list = []
        result = PersonalAccountAPI.session_request(method="POST", url=url, headers=headers,
                                                    body=body, params_flag=False)
        if result:
            supplier_id_list.extend(result[0][0]["result"]["suppliers"])
            return supplier_id_list
        else:
            return

    @staticmethod
    def get_x64_token(wb_token, supplier_id):
        url = WB_PERSONAL_ACCOUNT_API_URL + "/ns/supplier-card-api/portals/api/v1/statkey"

        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}; x-supplier-id={supplier_id}"
        headers["Referer"] = WB_PERSONAL_ACCOUNT_API_URL + "/supplier-settings/access-to-api"

        body = {}
        result = PersonalAccountAPI.session_request(method="POST", url=url, headers=headers,
                                                    body=body, params_flag=False)
        if result:
            key = result[0]["data"]["key64"]
            return key
        else:
            return

    @staticmethod
    def get_access_token(wb_token, supplier_id):
        url = WB_PERSONAL_ACCOUNT_API_URL + "/ns/public-api/suppliers-portal-eu/api/tokens/generateToken"

        headers = HEADERS_PERSONAL_ACCOUNT_API
        headers["Cookie"] = f"WBToken={wb_token}; x-supplier-id={supplier_id}"
        headers["Referer"] = WB_PERSONAL_ACCOUNT_API_URL + "/supplier-settings/access-to-new-api"

        body = {
            "id": "json-rpc_41",
            "jsonrpc": "2.0",
            "params":
                {
                    "supplierID": supplier_id,
                    "tokenName": "NewToken"
                }
        }

        result = PersonalAccountAPI.session_request(method="POST", url=url, headers=headers,
                                                    body=body, params_flag=False)
        if result:
            key = result[0]["result"]["token"]["accessToken"]
            return key
        else:
            return
        
