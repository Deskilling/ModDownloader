import requests
import json

# Simple Implementation of the Modrinth Api 
# Spagetti Code 

# Used to make requests 
def make_modrinth_request(endpoint):
    try:
        response = requests.get(f"https://api.modrinth.com{endpoint}")
        if not response.ok:
            print("Api Error")
            return None
        return json.loads(response.content)
    except (requests.RequestException, json.JSONDecodeError):
        return None

# Kinda useless but why not
def get_modrinth_api_version():
    respone = make_modrinth_request("")
    return respone["version"]

# Default Request Per Min 300
def get_remaining_requests():
    try:
        response = requests.get(f"https://api.modrinth.com/")
        if not response.ok:
            print("Api Error")
            return None
        else:
            return response.headers["x-ratelimit-remaining"]
    except (requests.RequestException, json.JSONDecodeError):
        return None

def get_mod_data(mod):
    return make_modrinth_request(f"/v2/project/{mod}")

def get_mod_versions_data(mod):
    return make_modrinth_request(f"/v2/project/{mod}/version")

def extract_mod_versions(mod_data):
    return mod_data["game_versions"]

def extract_mod_loaders(mod_data):
    return mod_data["loaders"]

# Realtalk wenn hier ein Error passiert dann juckt
# Kein Errol logging mfg
def extract_mod_url(version,loader,version_data):
    for i in version_data:
        if version in i.get("game_versions",[]):
            if loader in i.get("loaders",[]):
                for file in i.get("files",[]):
                    return file.get("url")
