import json

import requests


def fetch_systems():
    systems = requests.get('https://api.spacetraders.io/v2/systems.json')
    if systems.status_code == 503:
        return False
    data = systems.json()
    with open('systems.json', 'w') as f:
        json.dump(data, f)
    return True


def get_starting_systems():
    url = "https://api.spacetraders.io/v2/factions"
    querystring = {"limit": "20"}
    response = requests.get(url, params=querystring).json()
    hqs = [(d["symbol"], '-'.join(d["headquarters"].split("-")[:-1])) for d in response["data"]]
    return hqs
