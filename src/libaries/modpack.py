from libaries import util, modrinthapi
import json

def choose_modpack():
    util.check_path("../../modpacks/extracted")
    util.del_dir("../../modpacks/extracted")

    all_modpacks = util.listdir("../../modpacks")
    num_modpacks = len(all_modpacks)
    util.log(f"All modpacks found {num_modpacks} found: {all_modpacks}")

    if num_modpacks == 0:
        util.log("No modpacks found")
        print("No modpacks found")
        return False
    elif num_modpacks == 1:
        util.log("Only one modpack found")
        return all_modpacks[0]
    elif num_modpacks > 1:
        util.log("Multiple modpacks found")
        for i in range(num_modpacks):
            print(f"[{i+1}] {all_modpacks[i]}")
        option = input("Enter the number of the modpack you want to update: ")
        return all_modpacks[int(option)-1]

def extract_modpack(modpack):
    util.log("Extracting modpack")
    util.extract_zip(f"../../modpacks/{modpack}","../../modpacks/extracted")

def get_all_hashes():
    modpack_data = util.read_file("../../modpacks/extracted/modrinth.index.json")
    modpack_data = json.loads(modpack_data)

    all_hashes = []
    all_hashes_filenames = []

    for i in modpack_data["files"]:
        all_hashes.append(i["hashes"]["sha512"])
        all_hashes_filenames.append(i["path"])
    
    return all_hashes, all_hashes_filenames