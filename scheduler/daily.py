#!/usr/bin/python3.6
import sys

import requests

path = u'/home/undyingkingdoms/UndyingKingdoms'
if path not in sys.path:
    sys.path = [path] + sys.path

from scheduler import private_bearer_token

route = "https://undyingkingdoms.pythonanywhere.com/game_clock/advance_24h_analytics"

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
