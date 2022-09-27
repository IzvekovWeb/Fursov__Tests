from json import load
from config.constants import WARE_HOUSE


def get_ware_house() -> dict:
    with open(WARE_HOUSE, 'r', encoding='UTF-8') as json_file:
        return load(json_file)
