import requests

def find_address(adr):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'add_chains_loc': '1',
        'add_coords': '1',
        'add_rubrics_loc': '1',
        'bases': 'geo,biz,transit',
        'fullpath': '1',
        'lang': 'ru_RU',
        'origin': 'maps-search-form',
        'outformat': 'json',
        'part': f'{adr}',
        'pos': '11',
        'v': '9',
    }

    response = requests.get('https://suggest-maps.yandex.ru/suggest-geo', params=params, headers=headers)
    results = response.json()["results"]

    coords = list()
    user_response = list()
    for x in range(len(results)):
        if 'pos' in results[x]:
            user_response.append(f"{x + 1}. {results[x]['subtitle']['text'] + ', ' + results[x]['title']['text']}")
            crd = results[x]['pos'].split(',')
            coords.append(f"{crd[1]},{crd[0]}")
    
    return user_response, coords