import requests, json

def session_user(self, username, password):
    url = 'https://chillbet-api.com/graphql'

    headers = {
        'authority': 'chillbet-api.com',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': '',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://chillbet.net',
        'pragma': 'no-cache',
        'referer': 'https://chillbet.net/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    data = {
        'query': 'mutation oneClickLogin($username: String!, $password: String!) { oneClickLogin(username: $username, password: $password) {\n        __typename\naccessToken\nrefreshToken\n\n      } }',
        'variables': {'username': f'{username}', 'password': f'{password}'},
        'operationName': 'oneClickLogin'
    }

    response = requests.post(url, headers=headers, json=data)


    if response.status_code == 200:
        data = json.loads(response.text)
        accessToken = data['data']['oneClickLogin']['accessToken']
        refreshToken = data['data']['oneClickLogin']['refreshToken']
    else:
        print(f"Error: {response.status_code}")
    return accessToken, refreshToken
