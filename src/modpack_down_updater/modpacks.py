import ModrinthApi
import zipfile
import os


# Move to util prob
# Also used in update_via_hash
def check_dir():
    if not os.path.exists("../modpacks"):
        os.mkdir("../modpacks")
    return True

def get_all_mrpack():
    all_modspacks = os.listdir("../modpacks")
    print(all_modspacks)
    # TODO - Refactor for loop 
    # TODO - count ist eumler remove!!!
    count = 1

    for i in all_modspacks:
        print(f"[{count}] {i}")
        count += 1

def extract_mrpack(file):
    pass

def main():
    check_dir()
    print("Place your .mrpack file in modpacks/ \nPress Enter to Continue ")
    get_all_mrpack()
