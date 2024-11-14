from ModrinthApi import download_mod
from mod_downloader_with_config.config import check_config, get_input, update_config
import json

def download_from_config():
    with open('src/mod_downloader_with_config/config.json', 'r') as file:
        config = json.load(file)
        version = config.get("version",[])
        loader = config.get("loader",[])
        mods = config.get("mods",[])
        print(f"\n{version}")
        print(loader)
        print(mods)

        failedDownloads = []
        for i in range(len(mods)):
            output = download_mod(mods[i],version,loader,"output/config_download/")

            if output is mods[i]:
                failedDownloads.append(output)

        print(f"\n\nFinished Downloading")
        if failedDownloads is not None:
            print(f"Failed to Download {failedDownloads}")

def main():
    check_config()

    keep_config = input("Enter via Terminal? (This will overwrite your current config) \n(you can also edit the config.json)  y/n: ")
    if keep_config.lower() == "y":
        version, loader, mods = get_input()
        update_config(version,loader,mods)
    elif keep_config.lower() == "n":
        pass
    else:
        print("Please enter y or n")
        exit()

    download_from_config()