import requests

from mp_analytic.config.constants import WB_API_SUPPLIER_URL, SUPPLIERS
from mp_analytic.data.marketplaces.wildberries.wb_orders_statistics import OrdersStatisticsWB


def get_card_to_rename(nm, new_name):
    """
    :return: Response with card list
    """

    for supplier in SUPPLIERS.values():  # бежим по поставщикам
        response = OrdersStatisticsWB().get_cards(supplier)
        if not response:
            continue

        # Карточки запроса
        cards = response.json()['result']['cards']
        for cards_item in cards:
            for nomenclature_dict in cards_item['nomenclatures']:
                if nm != nomenclature_dict['nmId']:
                    continue
                else:
                    for addin in cards_item['addin']:
                        if addin['type'] == "Наименование":
                            addin['params'][0]['value'] = new_name
                            return cards_item, supplier


def request_rename_card():
    name = 'Юбка женская миди прямая с разрезом завышенной талией офисная модная классическая вечерняя базовая'
    nomenclature = 37756153
    changed_card, supplier = get_card_to_rename(nomenclature, name)
    changed_card.pop('batchID')
    changed_card['uploadID'] = supplier.get('supplier-id')
    update_card(changed_card, supplier)


def update_card(card, supplier):
    """
    :param supplier: Supplier
    :param card: Card
    :return: Response with part numbers
    """
    url = WB_API_SUPPLIER_URL + "/card/update"

    headers = {
        "Host": 'suppliers-api.wildberries.ru',
        "Content-Type": "application/json",
        "Authorization": supplier.get('token'),
    }

    body = {
        "id": 1,
        "jsonrpc": "2.0",
        "params": {
        }
    }

    timeout = 40
    session = requests.Session()

    if not supplier.get('old'):
        return None

    name = supplier.get("name")
    print(f"Сбор номенклатур для поставщика {name}")

    body['params']['supplierID'] = supplier.get('supplier-id')
    body['params']['card'] = card
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


if __name__ == '__main__':
    request_rename_card()
