#!/usr/bin/python3.6
from datetime import datetime
import sys

import requests

path = u'/home/undyingkingdoms/UndyingKingdoms'
if path not in sys.path:
    sys.path = [path] + sys.path

from scheduler import private_bearer_token

route = "https://undyingkingdoms.pythonanywhere.com/game_clock/advance_age"

if datetime.utcnow().weekday() == 2:
    print("Correct weekday for age reset")
    print("Current time:", datetime.utcnow())
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
else:
    print("No server reset today.")
