from libaries import util
import cli_menu

def main():
    util.change_exec_dir()
    util.create_logfile()

    util.all_folders()

    util.cls()

    running = True

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