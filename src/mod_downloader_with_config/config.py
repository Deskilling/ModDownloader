import os 

def generate_config():
    pass

def check_config():
    if os.path.exists("src/mod_downloader_with_config/config.json"):
        print("Found Config")
        file = open("src/mod_downloader_with_config/config.json").read()
        return True
    else:
        print("Missing Config")
        open("src/mod_downloader_with_config/config.json","x")
        config_structure = '{\n\t"version":"",\n\t"loader":"",\n\t"mods":[]\n}'
        file = open("src/mod_downloader_with_config/config.json","w")
        file.write(config_structure)
        print("Created Config")
        return True

def write_config(what,where):
    file = open("src/mod_downloader_with_config/config.json","w")
    file[where].write(what)

def get_input():
    version = input("Version: ")
    loader = input("Loader: ")
    mods = input("Your mods Example: mods, lithium, fabric-api: ")

check_config()
write_config("1.21","version")