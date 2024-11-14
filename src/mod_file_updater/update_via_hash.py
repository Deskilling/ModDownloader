# Add ModinthApi depedencies 
# TODO - Fix every import | Errors due working dir
import ModrinthApi 
import os

def get_all_mods():
    all_files = os.listdir("../../update_mods")
    all_hashes = []

    for i in range(len(all_files)):
        print(os.getcwd())
        all_hashes.append(ModrinthApi.sha1sum(all_files[i],"update_mods/"))

    print(all_hashes)

def check_dir():
    if os.path.exists("src/update_mods"):
        return True
    else:
        os.mkdir("src/update_mods")

def download_mod():
    pass

def info():
    input("Place all Mods you want to update in /update_mods/ \nWhen you are ready press Enter:")

check_dir()
get_all_mods()