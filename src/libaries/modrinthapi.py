import requests, json

def make_modrinth_request(endpoint):
    try:
        response = requests.get(f"https://api.modrinth.com{endpoint}")
        if not response.ok:
            print(f"Api Error on Endpoint {endpoint}")
            return None
        return response.json()
    except (requests.RequestException, json.JSONDecodeError):
        print(f"Request or JsonDecodeError {endpoint}")
        return None

def get_loader_and_versions(mod):
    response = make_modrinth_request(f"/v2/project/{mod}/version")
    return response["game_versions"], response["loaders"]

def get_mod_downloader(mod):
    response = make_modrinth_request(f"/v2/project/{mod}/version")
    return response["files"]["url"]