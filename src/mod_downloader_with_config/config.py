import json
import os


def generate_config():
    pass

# Hääääää
# Is richtig Arsch aber juckt
def check_config():
    if os.path.exists("src/mod_downloader_with_config/config.json"):
        print("Found Config")
        return True
    else:
        print("Missing Config")
        open("src/mod_downloader_with_config/config.json","x")
        config_structure = '{\n\t"version":"",\n\t"loader":"",\n\t"mods":[]\n}'
        file = open("src/mod_downloader_with_config/config.json","w")
        file.write(config_structure)
        print("Created Config")
        return True


# Clean wie die Sneaks von Red
def update_config(version=None, loader=None, mods=None):
    config = {
        "version": "",
        "loader": "",
        "mods": []
    }
    try:
        with open("src/mod_downloader_with_config/config.json", 'r') as file:
            config.update(json.load(file))
    except FileNotFoundError:
        pass

    if version is not None and loader is not None and mods is not None:
        config["version"] = version
        config["loader"] = loader
        config["mods"] = mods.split()

    with open("src/mod_downloader_with_config/config.json", 'w') as file:
        json.dump(config, file, indent=4)

def get_input():
    version = input("Version: ")
    loader = input("Loader: ")
    mods = input("Your mods Example: sodium lithium fabric-api: ")

    return version,loader,mods