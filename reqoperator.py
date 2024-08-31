import requests
import json
import re

def operator(TOKEN):
    url = 'https://chillbet-api.com/graphql'
    data = {
        "query": "mutation getSlotsGameUrl($id: String!, $currency: String) { getSlotsGameUrl(id: $id, currency: $currency) }",
        "variables": {
            "id": "new-double",
            "currency": "BRL"
        },
        "operationName": "getSlotsGameUrl"
    }

    header = {"Authorization":TOKEN}
    response = requests.post(url, headers=header, json=data)
    response = json.loads(response.text)

    # Extrair operatorId e authToken da resposta
    url = response['data']['getSlotsGameUrl']
    operator_id = re.search(r'operatorId=([\w-]+)', url).group(1)
    auth_token = re.search(r'authToken=([\w-]+)', url).group(1)
    print('op: ',operator_id)
    print('token: ',auth_token)
    return operator_id, auth_token
