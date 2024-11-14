import src.ModrinthApi
import os

def get_input():
    version = input("Version: ")
    loader = input("Loader: ")

    return version,loader

def update_all_mods(version,loader):
    all_files = os.listdir("update_mods/")
    all_hashes = []

    for i in range(len(all_files)):
        all_hashes.append(src.ModrinthApi.sha1sum(all_files[i],"update_mods/"))
        src.ModrinthApi.download_via_hash(all_hashes[i], version, loader)
    print(all_hashes)

def check_dir():
    if os.path.exists("update_mods"):
        return True
    else:
        os.mkdir("update_mods")
def main():
    check_dir()
    version, loader = get_input()
    input("Press Enter to Update every mod in update_mods ")
    update_all_mods(version,loader)