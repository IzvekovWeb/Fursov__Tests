import pytest


@pytest.fixture
def schema_get_user():
    return {
         "type": "object",
         "properties": {
             "price": {"type": ["number", "integer"]},
             "name": {"type": "string"},
             "username": {"type": "string"},
             "email": {"type": "string"},
             "full_name": {"type": "string"},
             "phone_num": {"type": ["string", "null"]},
             "date_follow": {"type": ["string", "null"]},
             "date_expire": {"type": ["string", "null"]},
             "tariff": {"type": ["string", "null"], "enum": ["Максимальный", "Оптимальный", "Базовый"]},
         },
         "required": ["email", "username", "tariff", "phone_num"]
    }


@pytest.fixture
def schema_analytic():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "update_at": {"type": ["string", "null"]},
            "sheet_title_id": {"type": "integer"},
            "sheet_name": {"type": "string"},
            "sheet_id": {"type": "string"},
            "spreadsheet_id": {"type": "string"},
            "spreadsheet_title": {"type": "string"},
            "has_detail": {"enum": ["False", "True"]},
            "secondary": {"enum": ["False", "True"]},
            "description": {"type": ["string", "null"]},
            "slug": {"type": "string"},
        },
        "required": ["id", "sheet_name", "sheet_id", "spreadsheet_id"]
    }


@pytest.fixture
def schema_analytic_tot():
    return {
        "type": "object",
        "properties": {
            "article": {"type": "string"},
            "nomenclature": {"type": "string"},
            "orders_amount": {"type": "integer"},
            "orders_rub": {"type": "number"}
        },
        "additionalProperties": False,
        "minProperties": 3
    }


@pytest.fixture
def schema_analytic_tog():
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "data": {"type": "array"}
        },
        "additionalProperties": False,
        "minProperties": 2
    }


@pytest.fixture
def schema_analytic_tbt():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "brand": {"type": "string"},
            "orders_amount": {"type": "integer"},
        },
        "additionalProperties": False,
        "minProperties": 3,
        "required": ["id", "brand", "orders_amount"]
    }


@pytest.fixture
def schema_analytic_bs():
    return {
        "type": "object",
        "properties": {
            "orders_amount": {"type": "integer"},
            "increase_amount": {"type": "integer"},
            "orders_rub": {"type": "integer"},
            "increase_rub": {"type": "integer"},
            "orders_sells": {"type": "integer"},
            "increase_sells": {"type": "integer"}
        },
        "additionalProperties": False,
        "minProperties": 6
    }


@pytest.fixture
def schema_analytic_tcd():
    return {
        "type": "object",
        "properties": {
            "category": {"type": "array"},
            "orders_rub": {"type": "array"},
        },
        "additionalProperties": False,
        "minProperties": 2
    }


@pytest.fixture
def schema_analytic_wrdo():
    return {
        "type": "object",
        "properties": {
            "dates": {"type": "array"},
            "orders_data": {"type": "array"},
            "sold_data": {"type": "array"},
        },
        "additionalProperties": False,
        "minProperties": 3
    }


@pytest.fixture
def schema_analytic_wrg():
    return {
        "type": "object",
        "properties": {
            "orders_rub": {"type": "number"},
            "realize": {"type": "number"},
            "logistic": {"type": "number"},
            "sold": {"type": "number"},
        },
        "additionalProperties": False,
        "minProperties": 4
    }


@pytest.fixture
def schema_analytic_wro():
    return {
        "type": "object",
        "properties": {
            "orders_count": {"type": "number"},
            "percent_fact": {"type": "number"}
        },
        "additionalProperties": False,
        "minProperties": 2
    }


@pytest.fixture
def schema_analytic_wrs():
    return {
        "type": "object",
        "properties": {
            "sold_count": {"type": "integer"},
            "percent_fact": {"type": "integer"}
        },
        "additionalProperties": False,
        "minProperties": 2
    }


@pytest.fixture
def schema_analytic_monthly_mrdo():
    return {
        "type": "object",
        "properties": {
            "dates": {"type": "array"},
            "orders_data": {"type": "array"},
            "sold_data": {"type": "array"},
        },
        "additionalProperties": False,
        "minProperties": 2
    }


@pytest.fixture
def schema_analytic_twc():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "orders_rub": {"type": "integer"},
        },
        "additionalProperties": False,
        "minProperties": 3,
        "required": ["id", "name"]

    }


@pytest.fixture
def schema_analytic_cbs():
    return {
        "type": "object",
        "properties": {
            "overall": {"type": "integer"},
            "overall_last_day": {"type": "integer"},
            "count": {"type": "integer"},
        },
        "additionalProperties": False,
        "minProperties": 3,
    }


@pytest.fixture
def schema_analytic_bsdo():
    return {
        "type": "object",
        "properties": {
            "orders_count": {"type": "integer"},
            "orders_rub": {"type": "integer"},
            "orders_rows": {"type": "integer"},
            "orders_zero": {"type": "integer"},
        },
        "additionalProperties": False,
        "minProperties": 4,
    }


@pytest.fixture
def schema_analytic_dow():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "date": {"type": "string"},
            "data": {"type": "integer"},
        },
        "additionalProperties": False,
        "minProperties": 3,
        "required": ["id", "data"]
    }


@pytest.fixture
def schema_analytic_tpp():
    return {
        "type": "object",
        "properties": {
            "name": {"type": "array"},
            "data": {"type": "array"},
        },
        "additionalProperties": False,
        "minProperties": 2,
        "required": ["name", "data"]
    }


@pytest.fixture
def schema_analytic_bsp():
    return {
        "type": "object",
        "properties": {
            "op": {"type": "integer"},
            "average_profit": {"type": "integer"},
            "prime_cost": {"type": "integer"},
            "logistics": {"type": "integer"},
            "storage": {"type": "integer"},
        },
        "additionalProperties": False,
        "minProperties": 5,
    }


@pytest.fixture
def schema_liquidity():
    return {
        "type": "object",
        "properties": {
            "data": {"type": "array"},
            "values": {"type": "array"},
        },
        "additionalProperties": False,
        "minProperties": 2,
    }
