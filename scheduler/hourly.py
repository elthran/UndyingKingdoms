#!/usr/bin/python3.6
import os
import sys

import requests

print(os.getcwd())

path = u'/home/undyingkingdoms/UndyingKingdoms/'
if path not in sys.path:
    sys.path = [path] + sys.path

from . import private_bearer_token

token = private_bearer_token.token
route = "https://undyingkingdoms.pythonanywhere.com/game_clock/advance"

r = requests.get(
    route,
    headers={"Authorization": "Bearer " + token}
)

try:
    print(r.json())
except Exception as e:
    print("Error:", e)
    print("Status code:", r.status_code)
    print("Response:", r.text)
