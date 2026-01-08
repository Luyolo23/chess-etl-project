import requests

def extract():
    username = "Larry23"
    url = f"https://lichess.org/api/games/user/{username}"

    params = {
        "max" : 50,
        "pgnInJson": True,
        "moves": True
    }

    headers = {
        "Accept": "application/x-ndjson"
    }

    response = requests.get(url, params=params, headers=headers)

    with open("raw_games.ndjson", "w") as f:
        f.write(response.text)

    print("Games downloaded!")