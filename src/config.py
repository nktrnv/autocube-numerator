import sys
from pathlib import Path

ADMIN_PASSWORD = "secrete"
YDB_ENDPOINT = "grpcs://ydb.serverless.yandexcloud.net:2135"
YDB_DATABASE = "/ru-central1/b1gco1s4ir1fq6mdcrf1/etnedgj1te4iojp9gbtt"
YDB_SERVICE_ACCOUNT_KEY = "key-ydb-sa.json"

BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", ".")).absolute()
