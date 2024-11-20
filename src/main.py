import os
import mod_downloader_with_config.mod_downloader as mod_downloader
import mod_file_updater.update_via_hash as update_via_hash
import modpack_down_updater.modpacks as modpacks
import ModrinthApi
from src.ModrinthApi import get_mod_data, get_mod_versions_data, extract_mod_loaders


# to make sure execution is happening in /src
# to fix import and directories
# IMMER EXECUTEN SONST TROLLT ALLES

def change_exec_dir():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
# main
def main():
    # wichtig
    change_exec_dir()

    option = input("[1] Mod Downloader Via Config \n[2] Download Update Mods with File \n[3] Update Modpack\ninput: ")

    if option == "1":
        mod_downloader.main()
    elif option == "2":
        update_via_hash.main()
    elif option == "3":
        modpacks.main()


# ka
if __name__ == "__main__":
    api_version = ModrinthApi.get_modrinth_api_version()
    if api_version is not None:
        print(f"Using ModrinthApi Version {api_version}")
        main()
    else:
        print("Error Requesting Api, Do you have Internet?")