import os
import sys
import pdb

from requests_html import HTMLSession

# path = u'/home/undyingkingdoms/UndyingKingdoms'
BASE_DIR = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])
if BASE_DIR not in sys.path:
    sys.path = [BASE_DIR] + sys.path

import private_config

def login(session, base):
    url = base + '/login/'
    r = session.get(url)
    csrf_token = r.html.find('#csrf_token', first=True).attrs['value']

    # pdb.set_trace()
    r = r.session.post(
        url,
        data=dict(
            csrf_token=csrf_token,
            email=private_config.MARLEN_TEMPORARY_EMAIL,
            password=private_config.MARLEN_TEMPORARY_ACCOUNT_PASSWORD,
        ),
        headers={
            "X-CSRF-TOKEN": csrf_token,
            "Referer": url
        }
    )
    return r


def cast_ligtening(r):
    LIGHTENING = 10
    TARGET = 3
    r = r.session.get(
        base + F"/gameplay/cast_spell/{LIGHTENING}/{TARGET}",
        headers={"Referer": base + F"/gameplay/casting/{TARGET}"}
    )
    return r


if __name__ == "__main__":
    session = HTMLSession()

    base = "https://undyingkingdoms.pythonanywhere.com"

    r = login(session, base)
    r = cast_ligtening(r)

    try:
        print(f"Autoplay worked! Last url {r.url}")
    except Exception as e:
        print("Error:", e)
        print("Status code:", r.status_code)
        print("Response:", r.text)
