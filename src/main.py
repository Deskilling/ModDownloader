import mod_downloader_with_config.mod_downloader
import mod_file_updater.update_via_hash

# mfg von Leif

def main():
    option = input("[1] Mod Downloader Via Config \n[2] Download Update Mods with File \ninput: ")

    if option == "1":
        mod_downloader_with_config.mod_downloader.main()
    elif option == "2":
        mod_file_updater.update_via_hash.main()

main()