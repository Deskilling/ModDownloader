import os, time
from libaries import util
from libaries import modrinthapi

def main():
    util.change_exec_dir()
    util.create_logfile()

    modrinthapi.get_all_hashes()
    #modrinthapi.cli_download()

    util.log("Finished Main")
    print("Finished Main")
    
main()