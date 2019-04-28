#!/usr/bin/python3.6
import sys

import requests

path = u'/home/undyingkingdoms/UndyingKingdoms'
if path not in sys.path:
    sys.path = [path] + sys.path

from scheduler import private_bearer_token
from config import SITE_URL

route = SITE_URL + "/game_clock/close_inactive_sessions"

r = requests.get(
    route,
    headers={"Authorization": "Bearer " + private_bearer_token.token}
)

try:
    print(r.json())
except Exception as e:
    print("Error:", e)
    print("Status code:", r.status_code)
    print("Response:", r.text)

