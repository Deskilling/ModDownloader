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

def latest_versions():
    # Used because fabric api will always give all versions for which fabric is available
    response = make_modrinth_request("/v2/project/fabric-api")
    if response is None:
        util.log("Error getting latest versions"); return None
    
    versions = response["game_versions"]
    versions = list(filter(lambda x: x.startswith("1."), versions))
    versions.sort() 

    extracted_versions = []

    for i in versions:
        if not "-" in i:
            extracted_versions.append(i)

    return extracted_versions

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
                util.log(f"File Name: {file_name}")
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

    return url, file_name

def download_multiple_hashes(all_hashes,all_hashes_filenames,version,loader):
    util.check_path("../../output")
    util.del_dir("../../output")
    util.check_path("../../output")

    failed_downloadhashes = []
    failed_files = []

    min = 1
    max = len(all_hashes)
    
    for i in all_hashes:
        util.cls()
        
        print(f"[{min}] {min*"#"}{(max-min)*"."} [{max}]")
        print(f"Current Mod: {all_hashes_filenames[min-1]}")

        url, file_name = get_download_via_hash(i,version,loader)

        if url is None or file_name is None:
            failed_file = all_hashes_filenames[all_hashes.index(i)]
            print(f"Error downloading: {failed_file}")
            print(f"Error downloading hash: {i}")
            util.log(f"Error downloading: {failed_file}")
            util.log(f"Error downloading hash: {i}\n")
            failed_downloadhashes.append(i)
            failed_files.append(failed_file)
        else:
            print(f"Downloading: {file_name}")
            util.log(f"Downloading: {file_name}\n")
            util.download_from_url(url,"../../output/",file_name)
        
        min += 1

    if len(failed_downloadhashes) > 0:
        util.cls()
        print("\nFailed to download:")
        util.log("Failed to download:")
        for i in failed_files:
            print(i)
            util.log(i) 