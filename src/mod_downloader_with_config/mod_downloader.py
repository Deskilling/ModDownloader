from ModrinthApi import download_mod
import mod_downloader_with_config.config as config
import json

def download_from_config():
    with open('mod_downloader_with_config/config.json', 'r') as file:
        config_data = json.load(file)
        version = config_data.get("version", "")
        loader = config_data.get("loader", "")
        mods = config_data.get("mods", [])

        failed_downloads = []
        for mod in mods:
            output = download_mod(mod, version, loader, "../output/config_download/")
            if output == mod:
                failed_downloads.append(output)

        print("\n\nFinished Downloading")
        if failed_downloads:
            print(f"Failed to Download {failed_downloads}")

def main():
    config.check_config()

    keep_config = input("Enter via Terminal? (This will overwrite your current config) \n(you can also edit the config.json)  y/n: ")
    if keep_config.lower() == "y":
        version, loader, mods = config.get_input()
        config.update_config(version, loader, mods)
    elif keep_config.lower() == "n":
        pass
    else:
        print("Please enter y or n")
        exit()

    download_from_config()
