from libaries import util, modrinthapi, modpack
import os

def cli_update_mods():
    util.cls()

    version = input("Enter Version for the Mods: ")
    util.log(f"Version: {version}")

    loader = input("Enter Loader for the Mods: ")
    util.log(f"Loader: {loader}")

    util.cls()

    util.check_path("../../mods_to_update")
    util.log("mods_to_update folder checked")

    input("Place all mods in the mods_to_update folder and press enter, note this will purge the curren output folder")
    # What da heeeel
    util.check_path("../../output")
    util.del_dir("../../output")
    util.check_path("../../output")
    
    util.log("Getting all hashes")
    all_hashes, all_hashes_filenames = util.get_all_hashes("../../mods_to_update/")
    
    modpack.download_multiple_hashes(all_hashes,all_hashes_filenames,version,loader)

def cli_update_modpack():
    util.cls()
    util.check_path("../../modpacks")
    util.log("modpacks folder checked or created")
    
    choosen_modpack = modpack.choose_modpack()
    modpack.extract_modpack(choosen_modpack)

    util.log("Getting all hashes")
    all_hashes, all_hashes_filenames = modpack.get_all_hashes()

    version = input("Enter Version for the Mods: ")
    util.log(f"Version: {version}")

    loader = input("Enter Loader for the Mods: ")
    util.log(f"Loader: {loader}\n")

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