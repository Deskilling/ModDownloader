import os, time
from libaries import util
from libaries import modrinthapi

def main():
    util.change_exec_dir()
    util.create_logfile()

    util.log("Apored")
    util.log("Gommehd")


    #versions, loaders = modrinthapi.get_loader_and_versions("sodium")

    print(modrinthapi.get_mod_downloader("eumelcrafter","1.21.1","fabric"))

    print("Finished Main")
main()