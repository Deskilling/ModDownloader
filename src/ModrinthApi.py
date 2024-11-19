from time import gmtime, strftime
import requests
import hashlib
import json
import os

# Simple Implementation of the Modrinth Api 
# Spagetti Code 

# Used for output directory
# TODO - Use pc time because different time eumler
datum = strftime("%d_%m_%Y_%H-%M-%S", gmtime())

# Used to make requests 
# Example: /v2/project/sodium ; /v2/version_file/{hash}
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

# Auf lecker schmecker
def get_mod_data(mod):
    request = make_modrinth_request(f"/v2/project/{mod}")
    if request is None:
        return None
    return request

# get all mod versions
# from get_mod_data()
def extract_mod_versions(mod_data):
    return mod_data["game_versions"]

# version data
def get_mod_versions_data(mod):
    request = make_modrinth_request(f"/v2/project/{mod}/version")
    # TODO - What da heeeel
    if request is None:
        return None
    return request

# alle loader halt locker checker
# TODO - Check for specific cases for project that switched loaders 
# Example Jade, glaube
def extract_mod_loaders(mod_data):
    return mod_data["loaders"]

# Prints should be useless
# Der macht mich Sauer
# TODO - Den Eumler besser machen (vllt version_data formaten)
def extract_mod_url(version,loader,version_data):
    for i in version_data:
        if version in i.get("game_versions",[]):
            if loader in i.get("loaders",[]):
                for file in i.get("files",[]):
                    return file.get("url"), file.get("filename")
            else:
                print(f"Loader: {loader} not Found")
                continue
        elif version not in version:
            print(f"Version {version} not Found")

    return None, None

# downloaded den aal auf versneakten Hasen in /output/datum/
def download_from_url(url, mod_name, path):
    # Create the target directory if it doesn't exist
    full_path = os.path.join(path + "_" + datum)
    os.makedirs(full_path, exist_ok=True)
    # Set the complete file path
    file_path = os.path.join(full_path, mod_name)

    # Download the file
    response = requests.get(url)
    if response.ok:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Error Downloading File: {mod_name}, URL: {url}")

# sha1 from file
# sha512 geht auch 
def sha1sum(filename,path):
    filename = path + filename
    with open(filename, 'rb', buffering=0) as f:
        return hashlib.file_digest(f, 'sha512').hexdigest()

# just get hash and requests auf lecker
# TODO - Return file name error 
# TODO - Fix muss prob in mod_file_updater gemacht werden
def download_via_hash(hashed_file, version, loader):
    response = make_modrinth_request(f"/v2/version_file/{hashed_file}")
    if response is None:
        print(f"Failed Download Hash:{hashed_file}, Version {version}, Loader {loader}")
        return None
    project_id = response["project_id"]

    return download_mod(project_id,version,loader,"../output/updated_hash")

# download mod without hash lecker hush
# TODO - Dieses goofy ass if xxx is None: irgendwie besser machen, aber geht so eig fit
def download_mod(mod,version,loader,path):
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
    download_from_url(url,filename,path)