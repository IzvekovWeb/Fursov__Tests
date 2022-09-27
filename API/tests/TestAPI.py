import os
import time
import pytest
import requests
import fake_useragent
from json import JSONDecodeError

from jsonschema import validate

from config.constants import GOOGLE_SHEETS_FILE
from google.sheet.sheet_api import GoogleSheetAPI

BASE_LINK = 'http://127.0.0.1:8000/api/v1'
EMAIL = "test@test.test"
PASSWD = "test"
user_agent = fake_useragent.UserAgent().random
HEADERS = {'user-agent': user_agent}


class TestLoginAPI:

    base_link = BASE_LINK
    # email = "igor.n.fursov@gmail.com"
    # passwd = "den"

    email = EMAIL
    passwd = PASSWD
    headers = HEADERS
    access_token = None
    refresh_token = None

    @pytest.fixture(autouse=True)
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

    def test_login(self):
        assert self.refresh_token is not None
        assert self.access_token is not None

    def test_refresh(self):
        old_access_token = self.access_token

        body = {"refresh": self.refresh_token}
        link = self.base_link + '/token/refresh'

        response_json = requests.post(link, data=body, headers=self.headers).json()

        self.access_token = response_json['access']
        assert old_access_token != self.access_token

    def test_logout(self):
        body = {"refresh": self.refresh_token}
        link = self.base_link + '/logout'

        response = requests.post(link, data=body, headers=self.headers)

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

        response = requests.get(link, headers=self.headers)

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

        response = requests.get(link, headers=self.headers)

        json_ = response.json()
        schema_analytic = request.getfixturevalue(expected)

        for item in json_:
            validate(item, schema_analytic)

    def test_analytics_put(self):
        sheet_pk = 1
        link = self.base_link + f'/analytic/wildberries/refresh/{sheet_pk}'

        response = requests.put(link, headers=self.headers)

        try:
            json_ = response.json()
        except JSONDecodeError:
            print('Response is not json')
            json_ = {"result": False}

        schema_analytics_put = {
            "type": "object",
            "properties": {
                "update_at": {"type": "string"}
            }
        }
        validate(json_, schema_analytics_put)

    def test_analytics_put_exception(self):
        sheet_pk = 10920123
        link = self.base_link + f'/analytic/wildberries/refresh/{sheet_pk}'

        response = requests.put(link, headers=self.headers)

        assert response.status_code == 406

    def test_week_plan_update(self):
        link = self.base_link + '/analytic/wildberries/week-plan-update'

        body = {
            "orders_rub": 1,
            "orders_count": 2,
            "sold_rub": 3,
            "sold_count": 4,
            "logistic": 5,
            "realize": 6,
            "sell_percent": 7
        }
        headers = self.headers
        headers['Content-Type'] = 'application/json'

        response = requests.put(link, json=body, headers=headers)

        assert response.status_code == 200, "Week plan wasn't updated"

        sheet_title = 'План'
        spreadsheet_id = '1FpTkzLG9arT82bgP_W-tDJ89HR3pbhBINIedG5EYJH4'
        sheet_id = '1666347203'
        spreadsheet_title = 'Wildberries'
        creds_ = os.path.join(r"C:\Users\sasiz\Desktop\Работа\Fursov\analytics-master\mp_analytic\config\credits.json")
        GSA = GoogleSheetAPI(
            sheet_title,
            spreadsheet_id,
            sheet_id,
            spreadsheet_title,
            creds_
        )

        result = GSA.get_row("A1", "G1", "План")
        assert result == [['1', '2', '3', '4', '5', '6', '7']], "No data in sheet, or it is not correct"

    def test_month_plan_update(self):
        link = self.base_link + '/analytic/wildberries/month-plan-update'

        body = {
            "orders_rub": 11,
            "orders_count": 22,
            "sold_rub": 33,
            "sold_count": 44,
            "logistic": 55,
            "realize": 66,
            "sell_percent": 77
        }
        headers = self.headers
        headers['Content-Type'] = 'application/json'

        response = requests.put(link, json=body, headers=headers)

        assert response.status_code == 200, "Month plan wasn't updated"

        sheet_title = 'План'
        spreadsheet_id = '1FpTkzLG9arT82bgP_W-tDJ89HR3pbhBINIedG5EYJH4'
        sheet_id = '1666347203'
        spreadsheet_title = 'Wildberries'
        creds_ = os.path.join(r"C:\Users\sasiz\Desktop\Работа\Fursov\analytics-master\mp_analytic\config\credits.json")
        GSA = GoogleSheetAPI(
            sheet_title,
            spreadsheet_id,
            sheet_id,
            spreadsheet_title,
            creds_
        )

        result = GSA.get_row("A4", "G4", "План")
        assert result == [['11', '22', '33', '44', '55', '66', '77']], "No data in sheet, or it is not correct"


