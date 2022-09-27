import datetime

import requests

from config.constants import WB_API_SUPPLIER_STATS_URL
from config.suppliers import SUPPLIERS


class SupplierStatAPI:
    """
    requests to https://suppliers-stats.wildberries.ru/api/v1/supplier
    """

    @staticmethod
    def get_orders(token, key, day, flag=1):
        """
        request to /orders

        :param token: auth token
        :param key: supplier key x64
        :param day: date of supplying
        :param flag: flag for request
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
                    print("Готово")
                    return response.json()
                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError) as e:
                print(e)
                session.close()
                session = requests.Session()
                timeout += 5


if __name__ == '__main__':
    sup = SUPPLIERS.get('fursov')
    SupplierStatAPI.get_orders(sup['token'], sup['x64key'], '2022-07-15', 'fursov')
