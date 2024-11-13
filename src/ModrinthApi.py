import requests
import json
import os
from time import gmtime, strftime


# Simple Implementation of the Modrinth Api 
# Spagetti Code 

datum = strftime("%d_%m_%Y_%H-%M-%S", gmtime())

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
    response = make_modrinth_request("")
    return response["version"]

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
# Kein Error logging mfg
def extract_mod_url(version,loader,version_data, versions):
    for i in version_data:
        if version in i.get("game_versions",[]):
            if loader in i.get("loaders",[]):
                for file in i.get("files",[]):
                    return file.get("url"),file.get("filename")
            else:
                print(f"Loader: {loader} not Found")
        elif version not in version:
            print(f"Version {version} not Found")

def  download_from_url(url,mod_name):

    # Example 13_11_2024_16-11-24
    os.makedirs(f"output/{datum}", exist_ok=True)
    file_path = os.path.join(f"output/{datum}", mod_name)
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        pass

def download_mod(mod,version,loader):
    mod_data = get_mod_data(mod)
    mod_version_data = get_mod_versions_data(mod)
    versions = extract_mod_versions(mod_data)
    loaders = extract_mod_loaders(mod_data)
    url, filename = extract_mod_url(version,loader,mod_version_data,version)
    print(f"Downloading: {filename}")
    download_from_url(url,filename)