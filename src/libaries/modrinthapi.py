import requests, json
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
    if response is None:
        util.log(f"Error finding: {mod}")
        print(f"Error finding: {mod}")
        return None

    util.log(f"Found game_versions: {response["game_versions"]}, loaders: {response["loaders"]}")
    return response["game_versions"], response["loaders"]

def get_mod_download_url(mod,version,loader):
    response = make_modrinth_request(f"/v2/project/{mod}/version")
    if response is None:
        util.log(f"Mod: {mod}, Version: {version}, Loader {loader} not found")
        return None, None

    for i in response:
        if version in i.get("game_versions",[]) and loader in i.get("loaders",[]):

                for file in i.get("files",[]):
                    url = file.get("url")
                    file_name = file.get("filename")
                    util.log(f"Found {mod}, {version},{loader}")
                    util.log(f"Url: {url}")
                    util.log(f"File Name: {file_name} \n")
                    return url, file_name
        else:
            util.log(f"Mod: {mod}, Version: {version}, Loader {loader} not found")
            return None, None

def get_download_via_hash(hash,version,loader):
    response = make_modrinth_request(f"/v2/version_file/{hash}")

    if response is None:
        util.log(f"Hash: {hash} not found")
        print(f"Hash: {hash} not found")
        return None, None

    project_id = response["project_id"]
    util.log(f"Hash: {hash}, Project_id {project_id}")
    url, file_name = get_mod_download_url(project_id,version,loader)

    if url is None or file_name is None:
        return None, None

    util.log(f"Url: {url}")
    return url, file_name