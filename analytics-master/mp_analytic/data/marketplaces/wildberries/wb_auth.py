import os
import re

import requests
from config.constants import DEFAULT_USER_AGENT, DEFAULT_TIMEOUT_VALUE, ATTEMPT_LIMIT, TIMEOUT_INCREMENTAL
from data.marketplaces.wildberries.wb_personal_account import PersonalAccountAPI
from data.marketplaces.wildberries.wb_wild_token import encode_token

WB_URL = "https://www.wildberries.ru/webapi/"
PARAMS = {
    'phoneInput.AgreeToReceiveSmsSpam': 'false',
    'phoneInput.ConfirmCode': '',
    'phoneInput.FullPhoneMobile': '',
    'returnUrl': 'https%3A%2F%2Fwww.wildberries.ru%2Flk',
    'phonemobile': '',
    'agreeToReceiveSms': 'false',
    'shortSession': 'false',
    'period': 'ru',
}


class WBAuth(object):
    def __init__(self, phone):
        self.__phone = phone
        self.__wild_token = None

    def request_confirm_code(self):
        url = WB_URL + "mobile/requestconfirmcode?forAction=EasyLogin"
        headers = {
            'User-Agent': DEFAULT_USER_AGENT
        }
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        session = requests.Session()

        PARAMS['phoneInput.FullPhoneMobile'] = self.__phone
        PARAMS['phonemobile'] = self.__phone

        while True:
            try:
                response = session.request("POST", url=url, headers=headers, params=PARAMS, timeout=timeout)
                if response.status_code == 200 and response.json():
                    return response.json().get("Value")
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return
                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    def post_confirm_code(self, code):
        url = WB_URL + "security/spa/signinsignup"
        headers = {
            'User-Agent': DEFAULT_USER_AGENT
        }
        timeout, attempt = DEFAULT_TIMEOUT_VALUE, 1
        session = requests.Session()

        PARAMS['phoneInput.FullPhoneMobile'] = self.__phone
        PARAMS['phonemobile'] = self.__phone
        PARAMS['phoneInput.ConfirmCode'] = code

        while True:
            try:
                response = session.request("POST", url=url, headers=headers, params=PARAMS, timeout=timeout)
                if response.status_code == 200 and response.json():
                    token = response.cookies.get("WILDAUTHNEW_V3")
                    return token
                if attempt == ATTEMPT_LIMIT:
                    print("Превышен лимит ожидания")
                    return
                attempt += 1
            except (requests.exceptions.RequestException, requests.exceptions.BaseHTTPError):
                session.close()
                session = requests.Session()
                attempt += 1
                timeout += TIMEOUT_INCREMENTAL

    def check_phone_number(self):
        if re.match(r"7\d{10}", self.__phone) and len(self.__phone) == 11:
            return True
        return False

    def get_wb_token(self, token_v3):
        # self.__wild_token = encode_token(token_v3 + os.environ.get("SECRET_TOKEN"))
        self.__wild_token = token_v3

        personal_acc = PersonalAccountAPI()
        wb_token = personal_acc.get_wb_token(wild_auth_token=token_v3)
        suppliers = personal_acc.get_supplier_id(wb_token)
        return wb_token, suppliers

    def get_external_keys(self, token, supplier_id):
        personal_acc = PersonalAccountAPI()
        x_key = personal_acc.get_x64_token(token, supplier_id)
        access_token = personal_acc.get_access_token(token, supplier_id)
        return x_key, access_token

    def get_wild_token(self):
        return self.__wild_token
