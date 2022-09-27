import requests

from config.constants import TIMEOUT_INCREMENTAL
from config.suppliers import OZON_SUPPLIERS


class OzonAPI:
    @staticmethod
    def get_category_title(supplier_id, supplier_token, category_id):
        url = 'https://api-seller.ozon.ru/v2/category/tree'
        headers = {'Client-Id': supplier_id, 'Api-Key': supplier_token}
        session = requests.Session()
        timeout = 40
        body= {'category_id': category_id}
        while True:
            try:
                response = session.request("POST", url, json=body, headers=headers, timeout=timeout)
                if response.status_code == 200:
                    data = response.json()
                    return data
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                timeout += TIMEOUT_INCREMENTAL

    @staticmethod
    def get_product_list(supplier_id, supplier_token):
        result = []
        url = 'https://api-seller.ozon.ru/v1/product/list'
        headers = {'Client-Id': supplier_id,
                   'Api-Key': supplier_token}
        session = requests.Session()
        timeout = 40
        while True:
            try:
                body = {"filter": {"visibility": "ALL"}, "page": 1, "page_size": 5000}
                response = session.request("POST", url, headers=headers, json=body, timeout=40)
                if response.status_code == 200:
                    res: dict = response.json()
                    result.extend(res.get('result').get('items'))
                    break

            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                timeout += TIMEOUT_INCREMENTAL
        return result

    @staticmethod
    def get_products_info(supplier_id, supplier_token, product_ids: list):
        url = 'https://api-seller.ozon.ru/v2/product/info/list'
        headers = {'Client-Id': supplier_id,
                   'Api-Key': supplier_token}
        session = requests.Session()
        timeout = 40
        body = {'product_id': product_ids}
        while True:
            response = session.request("POST", url, json=body, headers=headers, timeout=timeout)
            if response.status_code == 200:
                data = response.json().get('result').get('items')
                return data

    @staticmethod
    def get_orders(supplier_id, supplier_token, date_from, date_to):
        result = []
        url = 'https://api-seller.ozon.ru/v1/analytics/data'
        headers = {'Client-Id': supplier_id,
                   'Api-Key': supplier_token}
        session = requests.Session()
        timeout = 40
        limit = 1000
        offset = 0
        while True:
            body = {"date_from": date_from.strftime('%Y-%m-%d'),
                    "date_to": date_to.strftime('%Y-%m-%d'),
                    "metrics": ["revenue", "ordered_units"],
                    "dimension": ["day", 'sku'],
                    "limit": limit,
                    "offset": offset}
            response = session.request("POST", url, json=body, headers=headers, timeout=timeout)
            if response.status_code == 200:
                data = response.json().get('result').get('data')
                result.extend(data)
                if len(data) < 1000:
                    break
                offset += limit
        return result


if __name__ == '__main__':
    for supplier in OZON_SUPPLIERS.values():
        print(OzonAPI.get_product_list(supplier['client_id'], supplier['api_key']))
