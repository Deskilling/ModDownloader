from ModrinthApi import sha1sum, download_via_hash
import os

def get_input():
    version = input("Version: ")
    loader = input("Loader: ")
    return version, loader

def update_all_mods(version, loader):
    all_files = os.listdir("../update_mods/")
    all_hashes = []

    for file in all_files:
        file_hash = sha1sum(file, "../update_mods/")
        all_hashes.append(file_hash)
        download_via_hash(file_hash, version, loader)

def check_dir():
    if not os.path.exists("update_mods"):
        os.mkdir("update_mods")
    return True

def main():
    check_dir()
    version, loader = get_input()
    input("Press Enter to Update every mod in update_mods ")
    update_all_mods(version, loader)

    print()