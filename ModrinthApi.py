import requests
import json

# Kinda Utils
def extract_data(get,data):
    return data[get]

def make_modrinth_request(endpoint):
    try:
        response = requests.get(f"https://api.modrinth.com/v2/{endpoint}")
        if not response.ok:
            print("Api Error")
            return None
        return json.loads(response.content)
    except (requests.RequestException, json.JSONDecodeError):
        return None

def get_mod_data(mod):
    return make_modrinth_request(f"project/{mod}")

def get_mod_versions(mod):
    return make_modrinth_request(f"project/{mod}/version")

def extract_mod_download_url(version,loader,version_data):
    if version in version_data["game_versions"]:
        if loader in version_data["loaders"]:
            # TODO - Fix
            return version_data["files"][0]["url"]
        else:
            print(f"Loader: {loader}, not found")
            return None
    else:
        print(f"Version: {version}, not found")
        return None

extract_mod_download_url("1.20","fabric",get_mod_versions("jade"))