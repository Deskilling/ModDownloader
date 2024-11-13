from src.ModrinthApi import download_mod
import src.mod_downloader_with_config.config
from src.mod_downloader_with_config.config import check_config, get_input, update_config
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

        for i in range(len(mods)):
            download_mod(mods[i],version,loader)

def main():
    check_config()
    keep_config = input("Enter via Terminal? (you can also edit the config.json) y/n: ")
    if keep_config.lower() == "y":
        version, loader, mods = get_input()
        update_config(version,loader,mods)

    elif keep_config.lower() == "n":
        pass
    else:
        print("Please enter y or n")
        exit()

    download_from_config()