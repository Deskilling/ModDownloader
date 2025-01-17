from libaries import util, modrinthapi, modpack
import os

def get_user_versiond_and_loader():
    latest_version = modrinthapi.latest_versions()
    version = input(f"Enter Version for the Mods (default {latest_version[0]}): ")
    if version == "":
        version = latest_version[0]

    util.log(f"Version: {version}")

    loader = input("Enter Loader for the Mods (default fabric): ")
    if loader == "":
        loader = "fabric"
    util.log(f"Loader: {loader}")

    util.cls()

    return version, loader

def cli_update_mods():
    util.cls()

    version, loader = get_user_versiond_and_loader()

    util.check_path("../../mods_to_update")
    util.log("mods_to_update folder checked")

    input("Place all mods in the mods_to_update folder and press enter, note this will purge the curren output folder")
    # What da heeeel
    util.check_path("../../output")
    util.del_dir("../../output")
    util.check_path("../../output")
    
    util.log("Getting all hashes")
    all_hashes, all_hashes_filenames = util.get_all_hashes("../../mods_to_update/")
    
    modrinthapi.download_multiple_hashes(all_hashes,all_hashes_filenames,version,loader)

def cli_update_modpack():
    util.cls()
    util.check_path("../../modpacks")
    util.log("modpacks folder checked or created")

    choosen_modpack = modpack.choose_modpack()
    if len(choosen_modpack) > 1: 
        for i in choosen_modpack:
            print(f"[{choosen_modpack.index(i)+1}] {i}")
        
        option = int(input("Enter Number: ")) - 1
        choosen_modpack = choosen_modpack[option]
    else:
        # Housekeeping
        choosen_modpack = choosen_modpack[0]
    
    modpack.extract_modpack(choosen_modpack)

    util.log("Getting all hashes")
    all_hashes, all_hashes_filenames = modpack.get_all_hashes()

    util.cls()

    version, loader = get_user_versiond_and_loader()

    util.cls()

    modrinthapi.download_multiple_hashes(all_hashes,all_hashes_filenames,version,loader)

def cli_main():
    util.cls()

    print("Welcome to the Modupdater CLI")
    print("[1] Update Mods")
    print("[2] Update Modpack")
    print("[3] Exit")
    option = input("Enter your choice: ")

    if option == "1":
        cli_update_mods()
        input("\nPress Enter to continue")
        return False
    
    elif option == "2":
        cli_update_modpack()
        input("\nPress Enter to continue")
        return False
    
    elif option == "3":
        return False        