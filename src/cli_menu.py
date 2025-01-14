from libaries import util
from libaries import modrinthapi
import os

def cli_update_mods():
    util.cls()

    version = "1.21.3"#input("Enter Version for the Mods: ")
    util.log(f"Version: {version}")

    loader = "fabric"#input("Enter Loader for the Mods: ")
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
    
    failed_downloadhashes = []
    failed_files = []

    min = 0
    max = len(all_hashes)
    
    for i in all_hashes:
        url, file_name = modrinthapi.get_download_via_hash(i,version,loader)
        
        

        if url is None or file_name is None:
            failed_file = all_hashes_filenames[all_hashes.index(i)]
            print(f"Error downloading: {failed_file}")
            print(f"Error downloading hash: {i}")
            util.log(f"Error downloading: {failed_file}")
            util.log(f"Error downloading hash: {i}")
            failed_downloadhashes.append(i)
            failed_files.append(failed_file)
        else:
            print(f"Downloading: {file_name}")
            util.log(f"Downloading: {file_name}")
            util.download_from_url(url,"../../output/",file_name)

        util.cls()
        
        kriminelles_level = '.' * (max - min)
        kriminelles_level = '#' * min + kriminelles_level[max:]
        print(f"{min}/{max} [{kriminelles_level}]")
        min += 1

    if len(failed_downloadhashes) > 0:
        print("Failed to download:")
        util.log("Failed to download:")
        for i in failed_files:
            print(i)
            util.log(i) 

def cli_main():
    util.cls()

    print("Welcome to the Modrinth CLI")
    print("[1] Update Mods")
    print("[2] Exit")
    option = input("Enter your choice: ")

    if option == "1":
        cli_update_mods()
    elif option == "2":
        exit()