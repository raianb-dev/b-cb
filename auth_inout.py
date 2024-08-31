from reqoperator import operator
import requests, json


def auth_wss(TOKEN):
    op, auth = operator(TOKEN)
    url = 'https://api.inout.games/api/auth'

    data = {
    "operator": f"{op}",
    "auth_token": f"{auth}",
    "currency": "BRL"
    }

    header = {"Authorization":TOKEN}

    req = requests.post(url=url, json=data, headers=header)
    resp = json.loads(req.text)
    data = resp['result']
    return data