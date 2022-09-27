import requests

from config.constants import MP_STATS, DEFAULT_TIMEOUT_VALUE, DEFAULT_USER_AGENT, TIMEOUT_INCREMENTAL
from data.utils.functions import form_days_mpstats


def get_filter_body(filter_model, filter_type, filter_nm):
    return {"filterModel": {filter_model: {"filterType": filter_type, "type": "equals", "filter": filter_nm}}}


class MpStatsAPI:
    @staticmethod
    def get_sku_position(nomenclature_list):
        """
        get SKU position by nomenclatures
        :param nomenclature_list: nomenclatures
        :return: list of dicts with positions
        """
        result = []
        date_from, date_to = form_days_mpstats(7)

        session = requests.Session()
        headers = {'X-Mpstats-TOKEN': MP_STATS, 'User-Agent': DEFAULT_USER_AGENT, "Content-Type": "application/json"}
        params = {'d1': date_from, 'd2': date_to}
        timeout = DEFAULT_TIMEOUT_VALUE

        for nomenclature in nomenclature_list:
            if not isinstance(nomenclature, int):
                continue
            url = f'https://mpstats.io/api/wb/get/item/{nomenclature}/by_category'
            body = get_filter_body('id', 'number', nomenclature)
            while True:
                try:
                    response = session.request("GET", url, headers=headers, params=params, timeout=timeout, json=body)
                    if response.status_code == 200:
                        result.append({nomenclature: response.json()})
                        break
                    elif response.status_code == 500:  # if no data in mpstats.io
                        result.append(nomenclature)
                        print(f'По номенклатуре № {nomenclature} - нет данных!')
                        break
                except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                    session.close()
                    session = requests.Session()
                    timeout += TIMEOUT_INCREMENTAL
        return result

    @staticmethod
    def get_category(nomenclature_list, category):
        result = []
        date_from, date_to = form_days_mpstats(7)

        session = requests.Session()
        url = 'https://mpstats.io/api/wb/get/category'
        headers = {'X-Mpstats-TOKEN': MP_STATS, 'User-Agent': DEFAULT_USER_AGENT, "Content-Type": "application/json"}
        params = {'d1': date_from, 'd2': date_to, 'path': category}
        timeout = DEFAULT_TIMEOUT_VALUE

        for nomenclature in nomenclature_list:
            body = get_filter_body('id', 'text', nomenclature)
            while True:
                try:
                    response = session.request("POST", url, headers=headers, params=params, timeout=timeout, json=body)
                    if response.status_code == 200:
                        result.append(response.json())
                        break
                    elif response.status_code == 500:
                        result.append(nomenclature)
                        print(f'По номенклатуре № {nomenclature} - нет данных!')
                        break
                except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                    session.close()
                    session = requests.Session()
                    timeout += TIMEOUT_INCREMENTAL
        return result

    @staticmethod
    def get_category_by_date(columns):
        date_from, date_to = form_days_mpstats(7)
        url = f'https://mpstats.io/api/wb/get/category/by_date'
        headers = {'X-Mpstats-TOKEN': MP_STATS, 'Content-Type': 'application/json'}
        timeout = DEFAULT_TIMEOUT_VALUE
        session = requests.Session()
        for category in columns:
            params = {'d1': date_from, 'd2': date_to, 'path': category}
            while True:
                try:
                    response = session.get(url, headers=headers, params=params, timeout=timeout)
                    if response.status_code == 200:
                        return response.json()

                except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                    session.close()
                    session = requests.Session()
                    timeout += TIMEOUT_INCREMENTAL


if __name__ == '__main__':
    list_ = [113084844,
             113084779,
             74655479,
             63723610,
             63721616,
             63717793,
             63700666,
             63702148,
             63722555,
             63703159,
             74652466]

    print(MpStatsAPI.get_sku_position(list_))
