from os.path import abspath, dirname

WB_TOKEN = "Ava4vBeuqO2wDK7k1rEMQkc4V0Dq55fUNzBvwjJ7xmVCTp8ZjGvGKmeCSA4OoGfUbKQ08sHXFhDEMCScHnTrIG3VI1AKDMFoE_wCejftyUnFLQ"

WB_API_SUPPLIER_STATS_URL = "https://suppliers-stats.wildberries.ru/api/v1/supplier"
WB_API_SUPPLIER_URL = "https://suppliers-api.wildberries.ru"
WB_API_FEEDBACK_URL = "https://public-feedbacks.wildberries.ru/api/v1/summary/full"
WB_LOGISTIC_COST = 3.40896209

BASE_DIR = dirname(abspath(__file__))
ATTEMPT_LIMIT = 10000
DEFAULT_TIMEOUT_VALUE = 30
TIMEOUT_INCREMENTAL = 5
SELLER_HOST = 'seller.wildberries.ru'

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome' \
                     '/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36'
GOOGLE_SHEETS_FILE = BASE_DIR + '\\credits.json'
GOOGLE_SPREADSHEETS = BASE_DIR + '\\spreadsheets_max.json'
GOOGLE_SPREADSHEETS_MIN = BASE_DIR + '\\spreadsheets_min.json'
GOOGLE_SPREADSHEETS_OPT = BASE_DIR + '\\spreadsheets_opt.json'
GOOGLE_SHEETS_MANUAL = BASE_DIR + '\\manual_columns.json'
WARE_HOUSE = BASE_DIR + '\\ware_house.json'
APIS = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

MP_STATS = "624b45695be5e8.7515058633796de2caa5286346d385d7ee8dcec6"
