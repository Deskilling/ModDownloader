import tkinter
import tkinter.messagebox
import customtkinter
from libaries import util, modrinthapi, modpack
from time import sleep

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

def download_and_show_info(content_frame, all_hashes, all_hashes_filenames, version, loader):
    for widget in content_frame.winfo_children():
        widget.destroy()

    where = customtkinter.CTkLabel(content_frame, text=f"Downloading", font=("Arial", 20))
    where.pack(pady=10)

    progressbar = customtkinter.CTkProgressBar(content_frame, orientation="horizontal")
    progressbar.pack(pady=10)

    #status_label = customtkinter.CTkLabel(content_frame, text="")
    #status_label.pack(pady=10)

    util.check_path("../../output")
    util.del_dir("../../output")
    util.check_path("../../output")

    failed_downloadhashes = []
    failed_files = []

    min = 1
    max = len(all_hashes)

    for i in all_hashes:
        util.cls()
        
        print(f"[{min}] {min*"#"}{(max-min)*"."} [{max}]")
        print(f"Current Mod: {all_hashes_filenames[min-1]}")


        url, file_name = modrinthapi.get_download_via_hash(i,version,loader)

        currently_downloading = customtkinter.CTkLabel(content_frame, text=f"Downloading {file_name}")
        currently_downloading.pack(pady=10)

        if url is None or file_name is None:
            failed_file = all_hashes_filenames[all_hashes.index(i)]
            
            #status_label.configure(text=f"Error Downloading {file_name}")
            #content_frame.update_idletasks()
            
            util.log(f"Error downloading: {failed_file}")
            util.log(f"Error downloading hash: {i}\n")
            failed_downloadhashes.append(i)
            failed_files.append(failed_file)
        else:
            #status_label.configure(text=f"Downloading {file_name}")
            #content_frame.update_idletasks()

            util.log(f"Downloading: {file_name}\n")
            util.download_from_url(url,"../../output/",file_name)

        min += 1



# Für Mods
def get_version_and_loader_update_mods(content_frame, callback):
    for widget in content_frame.winfo_children():
        widget.destroy()

    where = customtkinter.CTkLabel(content_frame, text=f"Normal Modupdater", font=("Arial", 20))
    where.pack(pady=10)

    latest_version = modrinthapi.latest_versions()
    version_text = customtkinter.CTkLabel(content_frame, text=f"Version (default {latest_version[0]}):")
    version_text.pack(pady=10)
    version_entry = customtkinter.CTkEntry(content_frame)
    version_entry.pack(pady=10)

    loader_text = customtkinter.CTkLabel(content_frame, text="Loader (default fabric):")
    loader_text.pack(pady=10)
    loader_entry = customtkinter.CTkEntry(content_frame)
    loader_entry.pack(pady=10)

    loader_text = customtkinter.CTkLabel(content_frame, text="Place all of your mods in /mods_to_update")
    loader_text.pack(pady=10)

    def submit_input():
        version = version_entry.get() or latest_version[0]
        loader = loader_entry.get() or "fabric"

        util.log(f"Version: {version}")
        util.log(f"Loader: {loader}")

        all_hashes, all_hashes_filenames = util.get_all_hashes("../../mods_to_update/")

        download_and_show_info(content_frame, all_hashes, all_hashes_filenames, version, loader)

    knopf = customtkinter.CTkButton(content_frame, text="Enter", command=submit_input)
    knopf.pack(pady=10)

def update_mods(content_frame):
    util.cls()
    util.check_path("../../mods_to_update")
    #util.log("mods_to_update folder checked")

    def proceed_with_update(version, loader):
        util.check_path("../../output")
        util.del_dir("../../output")
        util.check_path("../../output")

        download_and_show_info(content_frame)

    # Request version and loader, then call proceed_with_update
    get_version_and_loader_update_mods(content_frame, proceed_with_update)


# For Modpacks
def get_version_and_loader_modpacks(content_frame, callback):
    for widget in content_frame.winfo_children():
        widget.destroy()

    where = customtkinter.CTkLabel(content_frame, text=f"Modpack Updater", font=("Arial", 20))
    where.pack(pady=10)

    modpacks_selector = customtkinter.CTkOptionMenu(master=content_frame, values=modpack.choose_modpack())
    modpacks_selector.pack(pady=20)

    latest_version = modrinthapi.latest_versions()
    version_text = customtkinter.CTkLabel(content_frame, text=f"Version (default {latest_version[0]}):")
    version_text.pack(pady=10)
    version_entry = customtkinter.CTkEntry(content_frame)
    version_entry.pack(pady=10)

    loader_text = customtkinter.CTkLabel(content_frame, text="Loader (default fabric):")
    loader_text.pack(pady=10)
    loader_entry = customtkinter.CTkEntry(content_frame)
    loader_entry.pack(pady=10)

    def submit_input():
        version = version_entry.get() or latest_version[0]
        loader = loader_entry.get() or "fabric"

        modpack_file = modpacks_selector.get()
        modpack.extract_modpack(modpack_file)
        all_hashes, all_hashes_filenames = modpack.get_all_hashes()

        download_and_show_info(content_frame, all_hashes, all_hashes_filenames, version, loader)
        

    knopf = customtkinter.CTkButton(content_frame, text="Enter", command=submit_input)
    knopf.pack(pady=10)

def update_modpack(content_frame):
    util.cls()
    util.check_path("../../modpacks")

    def proceed_with_modpack_update(version, loader):
        choosen_modpack = modpack.choose_modpack()
        modpack.extract_modpack(choosen_modpack)
        all_hashes, all_hashes_filenames = modpack.get_all_hashes()
        modrinthapi.download_multiple_hashes(all_hashes, all_hashes_filenames, version, loader)

    get_version_and_loader_modpacks(content_frame, proceed_with_modpack_update)

def main():
    # root
    root = customtkinter.CTk()
    root.title("Mod Updater GUI")
    root.geometry("800x400")

    # sidebar
    sidebar = customtkinter.CTkFrame(root, width=200)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)

    # logo
    modupdater_text = customtkinter.CTkLabel(sidebar, text="Mod Updater", font=customtkinter.CTkFont(size=20, weight="bold"))
    modupdater_text.pack(pady=(20, 10))

    main_frame = customtkinter.CTkFrame(root)
    main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    hallihallo = customtkinter.CTkLabel(main_frame, text="Welcome to the Mod Updater!\nChoose an option from the left.", font=customtkinter.CTkFont(size=18))
    hallihallo.pack(pady=20)

    update_mods_button = customtkinter.CTkButton(sidebar, text="Update Mods", command=lambda: update_mods(main_frame))
    update_mods_button.pack(pady=10, padx=10)

    update_modpack_button = customtkinter.CTkButton(sidebar, text="Update Modpack", command=lambda: update_modpack(main_frame))
    update_modpack_button.pack(pady=10, padx=10)

    exit_button = customtkinter.CTkButton(sidebar, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    util.change_exec_dir()
    util.create_logfile()
    main()