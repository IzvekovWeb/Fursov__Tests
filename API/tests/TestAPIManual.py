import time
from json import JSONDecodeError

import pytest
import requests

from TestAPI import HEADERS, BASE_LINK, EMAIL, PASSWD


class TestConfirmAPI:
    headers = HEADERS
    base_link = BASE_LINK

    @pytest.fixture(autouse=True, scope="class")
    def login(self, email=EMAIL, passwd=PASSWD):
        self.email = email
        self.passwd = passwd

        body = {"email": self.email, "password": self.passwd}
        link = self.base_link + '/login'

        response_json = requests.post(link, data=body, headers=self.headers).json()

        self.access_token = response_json['access']
        self.refresh_token = response_json['refresh']

        print(self.access_token)

        self.headers["Authorization"] = f"Bearer {self.access_token}"

    def test_request_confirm(self):

        link = self.base_link + f'/request-confirm'
        body = {'phone_num': "79266693918"}

        response = requests.put(link, json=body, headers=self.headers)

        expected = ["Код для авторизации отправлен в раздел «Уведомления» Личного кабинета. Посмотрите его на других авторизованных устройствах или запросите код на телефон.",
                    "Код выслан на номер"]

        assert response.text == "Код выслан на номер"


class TestUserAPI:
    """
    WARNING!!!

    This test class create new users in system!

    Sometimes it can fail, if username already exists, because of randomizer.
    """
    base_link = BASE_LINK

    def test_registration_and_post_info(self):
        link = self.base_link + '/register'
        rand_number = str(time.time())[-4:]

        body = {
            "email": f"test@{rand_number}.test",
            "username": f"test_{rand_number}",
            "password": "test"
        }

        response = requests.post(link, data=body, headers=HEADERS)

        assert response.status_code == 201, "User wasn't created"

        body_login = body
        body_login.pop('username')

        link = self.base_link + '/login'

        response_login = requests.post(link, data=body_login, headers=HEADERS)

        assert response_login.status_code == 200, "User is not exists"
        assert response_login.json()['access'], "Some problems with access token"

        headers = HEADERS
        headers['Authorization'] = f"Bearer {response_login.json()['access']}"
        headers['Content-Type'] = 'application/json'

        body_user = {
            "full_name": "full_name",
            "phone_num": "79797779976"
        }

        link = self.base_link + '/user'

        response_user = requests.post(link, json=body_user, headers=headers)

        try:
            json_ = response_user.json()
        except JSONDecodeError:
            json_ = {'message': False}

        assert json_['message'] == 'Success!', "Full name and phone wasn't updated"