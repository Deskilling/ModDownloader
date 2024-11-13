from time import gmtime, strftime
import requests
import json
import os

# Simple Implementation of the Modrinth Api 
# Spagetti Code 

# Used for output directory
datum = strftime("%d_%m_%Y_%H-%M-%S", gmtime())

# Used to make requests 
def make_modrinth_request(endpoint):
    try:
        response = requests.get(f"https://api.modrinth.com{endpoint}")
        if not response.ok:
            print(f"Api Error on Endpoint {endpoint}")
            return None
        return json.loads(response.content)
    except (requests.RequestException, json.JSONDecodeError):
        print(f"Request or JsonDecodeError {endpoint}")
        return None

# Kinda useless but why not
def get_modrinth_api_version():
    response = make_modrinth_request("")
    if response is None:
        print("Failed to Get Api Version")
        return None
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
    request = make_modrinth_request(f"/v2/project/{mod}")
    if request is None:
        return None
    return request

def extract_mod_versions(mod_data):
    return mod_data["game_versions"]

def get_mod_versions_data(mod):
    request = make_modrinth_request(f"/v2/project/{mod}/version")
    if request is None:
        return None
    return request

def extract_mod_loaders(mod_data):
    return mod_data["loaders"]

# Prints should be useless
def extract_mod_url(version,loader,version_data):
    for i in version_data:
        if version in i.get("game_versions",[]):
            if loader in i.get("loaders",[]):
                for file in i.get("files",[]):
                    return file.get("url"), file.get("filename")
            else:
                print(f"Loader: {loader} not Found")
                return None, None
        elif version not in version:
            print(f"Version {version} not Found")
            return None, None

def download_from_url(url,mod_name):
    os.makedirs(f"output/{datum}", exist_ok=True)
    file_path = os.path.join(f"output/{datum}", mod_name)

    response = requests.get(url)
    # 200 ist Cringe .ok ist cooler mfg
    if response.ok:
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Error Downloading File: {mod_name}, Url: {url}")

def download_mod(mod,version,loader):
    mod_data = get_mod_data(mod)
    if mod_data is None:
        print(f"Error getting {mod} data")
        return mod

    mod_version_data = get_mod_versions_data(mod)
    if mod_version_data is None:
        print(f"Error getting {mod} versions")
        return mod

    all_mod_versions = extract_mod_versions(mod_data)
    if version not in all_mod_versions:
        print(f"Version {version} not available for {mod} \nall available versions {all_mod_versions}")
        return mod

    loaders = extract_mod_loaders(mod_data)
    if loader not in loaders:
        print(f"Loader {loader} not available for {mod} with the Version {version} \nall available loaders {loaders}")
        return mod

    url, filename = extract_mod_url(version,loader,mod_version_data)
    if url is None:
        print("Url is None")
        return mod

    if filename is None:
        print(f"Filename is None")
        return mod

    print(f"Downloading: {filename}")
    download_from_url(url,filename)