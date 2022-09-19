import pytest
import requests
import fake_useragent

from jsonschema import validate

from urllib3.exceptions import HTTPError
from pprint import pprint


class TestAPI:

    base_link = "https://market-dt.ru/api/v1"
    email = "igor.n.fursov@gmail.com"
    passwd = "den"
    user_agent = fake_useragent.UserAgent().random
    HEADERS = {'user-agent': user_agent}
    access_token = None
    refresh_token = None

    @pytest.fixture(autouse=True)
    def login(self, email=email, passwd=passwd):

        self.email = email
        self.passwd = passwd

        body = {"email": self.email, "password": self.passwd}
        link = self.base_link + '/login'

        response_json = requests.post(link, data=body, headers=self.HEADERS).json()

        self.access_token = response_json['access']
        self.refresh_token = response_json['refresh']

        self.HEADERS["Authorization"] = f"Bearer {self.access_token}"

    def test_login(self):
        assert self.refresh_token is not None
        assert self.access_token is not None

    def test_refresh(self):
        old_access_token = self.access_token

        body = {"refresh": self.refresh_token}
        link = self.base_link + '/token/refresh'

        response_json = requests.post(link, data=body, headers=self.HEADERS).json()

        self.access_token = response_json['access']

        assert old_access_token != self.access_token

    def test_logout(self):
        body = {"refresh": self.refresh_token}
        link = self.base_link + '/logout'

        response = requests.post(link, data=body, headers=self.HEADERS)

        assert response.status_code == 204

    def test_user(self):
        body = {
            "full_name": "value",
            "phone_num": "value"
        }
        link = self.base_link + '/user'

        response = requests.post(link, data=body, headers=self.HEADERS)

        assert response.status_code == 204

    @pytest.mark.parametrize("link, expected", [
        ('/user', 'schema_get_user'),
        ('/analytic/dashboard/base-statistic', 'schema_analytic_bs'),
        ('/analytic/dashboard/top-categories-donut', 'schema_analytic_tcd'),
        ('/analytic/wildberries/weekly-report-dynamic-orders', 'schema_analytic_wrdo'),
        ('/analytic/wildberries/weekly-report-goto', 'schema_analytic_wrg'),
        ('/analytic/wildberries/weekly-report-orders', 'schema_analytic_wro'),
        ('/analytic/wildberries/weekly-report-sold', 'schema_analytic_wrs'),
        ('/analytic/wildberries/monthly-report-dynamic-orders', 'schema_analytic_wrdo'),
        ('/analytic/wildberries/monthly-report-goto', 'schema_analytic_wrg'),
        ('/analytic/wildberries/monthly-report-orders', 'schema_analytic_wro'),
        ('/analytic/wildberries/monthly-report-sold', 'schema_analytic_wrs'),
        ('/analytic/wildberries/categories-base-stat', 'schema_analytic_cbs'),
        ('/analytic/wildberries/base-stat-dynamic-orders', 'schema_analytic_bsdo'),
        ('/analytic/wildberries/top-profit-profitability', 'schema_analytic_tpp'),
        ('/analytic/wildberries/worst-profit-profitability', 'schema_analytic_tpp'),
        ('/analytic/wildberries/base-stat-profitability', 'schema_analytic_bsp'),
        ('/analytic/wildberries/liquidity/rent-days', 'schema_liquidity'),
        ('/analytic/wildberries/liquidity/rent-remains', 'schema_liquidity'),
        ('/analytic/wildberries/liquidity/liquid-remains', 'schema_liquidity'),
        ('/analytic/wildberries/liquidity/liquid-rent', 'schema_liquidity'),
        ('/analytic/wildberries/abc/rent', 'schema_liquidity'),
        ('/analytic/wildberries/abc/days', 'schema_liquidity'),
        ('/analytic/wildberries/abc/conclusion', 'schema_liquidity'),
        ('/analytic/wildberries/month', 'schema_analytic'),

    ])
    def test_get_dict(self, link, expected, request):

        link = self.base_link + link

        response = requests.get(link, headers=self.HEADERS)

        json_ = response.json()
        schema_user = request.getfixturevalue(expected)

        validate(json_, schema_user)

    @pytest.mark.parametrize("link, expected", [
        ('/analytic/wildberries', 'schema_analytic'),
        ('/analytic/dashboard/top-orders-table', 'schema_analytic_tot'),
        ('/analytic/dashboard/top-orders-graph', 'schema_analytic_tog'),
        ('/analytic/dashboard/top-brands-table', 'schema_analytic_tbt'),
        ('/analytic/wildberries/top-worst-categories', 'schema_analytic_twc'),
        ('/analytic/wildberries/top-categories-graph', 'schema_analytic_tog'),
        ('/analytic/wildberries/dynamic-orders-week', 'schema_analytic_dow'),

    ])
    def test_get_list(self, link, expected, request):
        link = self.base_link + link

        response = requests.get(link, headers=self.HEADERS)

        json_ = response.json()
        schema_analytic = request.getfixturevalue(expected)

        for item in json_:
            validate(item, schema_analytic)
