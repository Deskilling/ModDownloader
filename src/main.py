﻿import cli_menu, tgui_menu
from libaries import util
from libaries import modrinthapi

def main():
    util.change_exec_dir()
    util.create_logfile()

    util.cls()

    tgui_menu.main()

    running = False

    while running:
        should_run = cli_menu.cli_main()
        if not should_run:
            running = False
        else:
            running = True

    util.log("Finished Main")
    print("\nFinished Main")

if __name__ == '__main__':
    main()