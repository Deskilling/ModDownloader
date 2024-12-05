import requests, json, os
from libaries import util

def make_modrinth_request(endpoint):
    try:
        response = requests.get(f"https://api.modrinth.com{endpoint}")
        if not response.ok:
            util.log(f"Api Error on Endpoint {endpoint}")
            return None
        return response.json()
    except (requests.RequestException, json.JSONDecodeError):
        util.log(f"Request or JsonDecodeError {endpoint}")
        return None

def get_loader_and_versions(mod):
    response = make_modrinth_request(f"/v2/project/{mod}")
    return response["game_versions"], response["loaders"]

def get_mod_downloader(mod,version,loader):
    response = make_modrinth_request(f"/v2/project/{mod}/version")

    if response is None:
        util.log(f"Mod: {mod}, Version: {version}, Loader {loader} not found")
        return f"Mod: {mod}, Version: {version}, Loader {loader} not found"

    for i in response:
        if version in i.get("game_versions",[]):
            if loader in i.get("loaders",[]):
                for file in i.get("files",[]):
                    return file.get("url"), file.get("filename")

