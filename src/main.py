import mod_downloader_with_config.mod_downloader
import mod_file_updater.update_via_hash

# mfg von Leif

def main():
    #mod_downloader_with_config.mod_downloader.main()
    mod_file_updater.update_via_hash.check_dir()
    mod_file_updater.update_via_hash.get_all_mods()


main()