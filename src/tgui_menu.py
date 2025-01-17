import tkinter
import tkinter.messagebox
import customtkinter
import threading
from libaries import util, modrinthapi, modpack

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


def download_and_show_info(content_frame, all_hashes, all_hashes_filenames, version, loader):
    util.cls()

    for widget in content_frame.winfo_children():
        widget.destroy()

    where = customtkinter.CTkLabel(content_frame, text=f"Downloading", font=("Arial", 20))
    where.pack(pady=10)

    progressbar = customtkinter.CTkProgressBar(content_frame, width=300, height=10, border_width=2, corner_radius=10, orientation="horizontal", mode="determinate")
    progressbar.pack(pady=20)

    downloading_label = customtkinter.CTkLabel(content_frame, text=f"")
    downloading_label.pack(pady=0)

    util.check_path("../../output")
    util.del_dir("../../output")
    util.check_path("../../output")

    failed_downloadhashes = []
    failed_files = []
    
    minimal = 1
    maximal = len(all_hashes)

    progressbar.set(0)

    def update_progress(i):
        progress = (i + 1) / maximal
        progressbar.set(progress)
        content_frame.update_idletasks()

    def threaded_download():
        nonlocal minimal, where, progressbar, downloading_label
        for i, file_hash in enumerate(all_hashes):
            util.cls()
            update_progress(i)
            print(f"[{minimal}] {minimal * '#'}{(maximal - minimal) * '.'} [{maximal}]")
            print(f"Current Mod: {all_hashes_filenames[minimal - 1]}")

            url, file_name = modrinthapi.get_download_via_hash(file_hash, version, loader)

            if url is None or file_name is None:
                failed_file = all_hashes_filenames[i]
                util.log(f"Error downloading: {failed_file}")
                util.log(f"Error downloading hash: {file_hash}\n")
                failed_downloadhashes.append(file_hash)
                failed_files.append(failed_file)

                downloading_label.destroy()
                downloading_label = customtkinter.CTkLabel(content_frame, text=f"{failed_file}")
                downloading_label.pack(pady=10)

            else:
                util.log(f"Downloading: {file_name}\n")
                util.download_from_url(url, "../../output/", file_name)

                downloading_label.destroy()
                downloading_label = customtkinter.CTkLabel(content_frame, text=f"{file_name}")
                downloading_label.pack(pady=10)

            minimal += 1

        print("Download complete!")
        #!??!
        progressbar.destroy()

        for b in failed_files:
            failed_files_label = customtkinter.CTkLabel(content_frame, text=f"{b}")
            failed_files_label.pack(pady=10)

    threading.Thread(target=threaded_download, daemon=True).start()

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