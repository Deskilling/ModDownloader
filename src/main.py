import cli_menu
from libaries import util

def main():
    util.change_exec_dir()
    util.create_logfile()

    while True:
        cli_menu.cli_main()

    util.log("Finished Main")
    print("\nFinished Main")

if __name__ == '__main__':
    main()