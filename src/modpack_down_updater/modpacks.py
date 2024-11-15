import ModrinthApi
import zipfile
import os

def check_dir():
    if not os.path.exists("../modpacks"):
        os.mkdir("../modpacks")
    return True

def get_all_mrpack():
    pass

def extract_mrpack(file):
    pass

def main():
    check_dir()
    print("Place your .mrpack file in modpacks/")
