import os
from libaries import util
from libaries import modrinthapi




def main():
    util.change_exec_dir()
    print(modrinthapi.get_loader_and_versions("sodium"))
    print(modrinthapi.get_mod_downloader("sodium"))

    print("Finished Main")

main()