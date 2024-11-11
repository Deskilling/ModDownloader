import requests
import json

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

def get_mod_available_versions(mod):
    return make_modrinth_request(f"project/{mod}/version")

def extract_mod_versions(version_data):
    versions = set()
    for i in version_data:
        versions.update(i.get("game_versions",[]))
    return versions

def extract_mod_loaders(version_data):
    loader = set()
    for i in version_data:
        loader.update(i.get("loaders", []))
    return loader

def extract_mod_download_url(version, loader, versions_data,all_versions):
    for entry in versions_data:
        if version in entry.get("game_versions", []):
            if loader in entry.get("loaders", []):
                for file in entry.get("files", []):
                    if file.get("primary", False):
                        return file.get("url")
            else:
                print("Loader is not supported for that version")
        elif version not in all_versions:
            print("Version not Found")
            break

    return None
