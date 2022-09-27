import requests
from config.constants import WB_API_SUPPLIER_STATS_URL, ATTEMPT_LIMIT


class SupplierStatAPI:
    """
    requests to https://suppliers-stats.wildberries.ru/api/v1/supplier
    """

    @staticmethod
    def get_orders(token, key, day, flag=1):
        """
        request to /orders\n
        :param token: auth token
        :param key: supplier key x64
        :param day: date of supplying
        :param flag: flag for request
        :return: json
        """
        url = WB_API_SUPPLIER_STATS_URL + '/orders'

        headers = {'Authorization': token, 'User-Agent': 'Mozilla/5.0'}  # request headers
        params = {'dateFrom': day, 'key': key, 'flag': flag}  # request params
        timeout = 30  # request timeout
        session = requests.Session()
        attempt = 1

        while True:
            try:
                response = session.request("GET", url=url, headers=headers, params=params, timeout=timeout)
                if response.status_code == 200:
                    return response.json()
                attempt += 1
                if attempt == ATTEMPT_LIMIT:
                    return
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError) as e:
                print(e)
                session.close()
                session = requests.Session()
                timeout += 5

    @staticmethod
    def report_detail_by_period(supplier, dates):
        url = WB_API_SUPPLIER_STATS_URL + '/reportDetailByPeriod'

        headers = {
            "Content-Type": "application/json",
            "Authorization": supplier.get('token'),
        }

        timeout = 120
        session = requests.Session()
        limit = 100000

        url += f'?dateFrom={dates[0]}' \
               f'&key={supplier.get("x64key")}' \
               f'&limit={limit}' \
               f'&dateTo={dates[1]}'

        while True:
            try:
                response = session.get(url=url, headers=headers, timeout=timeout)
                if response.status_code == 200:
                    break
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                timeout += 5
        result = response.json()
        return result
