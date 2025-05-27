from tkinter import *
from sys import exit
import sys
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import threading
from sys import exit
from tkinter.font import Font
from tkinter import messagebox as mb
import os
from time import sleep
import requests
import json
import zipfile

#Class

class MrpackIndexer:
    def __init__(self, f_path):
        print(f_path)
        self.file_path = f_path

        # Open file
        with zipfile.ZipFile(self.file_path, "r") as z:
            # Read data
            with z.open('modrinth.index.json', 'r') as f:
                json_bytes = f.read()

            json_str = json_bytes.decode('utf-8')

            data = json.loads(json_str)

            # Get mods
            mods = data['files']

            # Make a list of the mods
            self.mods_dir = {}
            loops = 0
            for mod in mods:
                i = data['files'].index(mod)
                self.mods_dir[data['files'][i]['path'].strip('mods/')] = data['files'][i]['downloads'][0]
                loops += 1

            # Assign variables
            self.name = data["name"]
            self.description = data["summary"]
            self.version = data["dependencies"]["minecraft"]
            self.mod_id = self.name.lower().replace(" ", "")
            loader_type = list(data["dependencies"].keys())[1]
            self.loader = loader_type + '-' + data["dependencies"][loader_type] + '-' + self.version
            self.mod_count = loops

class ModIndexer:
    def __init__(self, f_path):
        print(f_path)
        self.file_path = f_path

        # Open file
        with open(self.file_path, "r") as f:
            # Read data
            data = json.load(f)

            # Get mods
            mods = data["mods"]

            # Make a list of the mods
            self.mods_dir = {}
            loops = 0
            for mod in mods:
                self.mods_dir[mod] = mods[mod]
                loops += 1

            # Assign variables
            self.name = data["name"]
            self.description = data["description"]
            self.mod_id = data["id"]
            self.version = data["version"]
            self.loader = data["loader"]
            self.creator = data["creator"]
            self.mod_count = loops

    def sus(self):
        print(self.file_path)


# Variables and default directory

progress = False

user = os.getlogin()
app_directory = f"C:\\Users\\{user}\\AppData\\Roaming\\.mod-installer\\"
install_path = app_directory + "clients"

launcher_profiles = f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\launcher_profiles.json"
installed_versions_path = f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\versions"

# Functions and shit

def json_read(file):
    with open(file, "r") as f:
        return json.load(f)


def json_write(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)
        return True


def install():
    global progress
    root.destroy()
    progress = True


def destroy():
    root.destroy()
    quit()


def browse_button():
    filename = filedialog.askdirectory()
    if filename != "":
        data = json_read(app_directory + "data.json")
        data["default_directory"] = filename
        json_write(data, app_directory + "data.json")
        gui_path.set(filename)

# Root
root = Tk()

if len(sys.argv) > 1:
    file_path = sys.argv[1]
    if ''.join(list(file_path)[-6:]) == "mrpack":
        print("MR PACK DECTED")
        mb.showinfo(title='Warning',
                    message="The pack you are trying to install is an mrpack, mrpacks have limited support.")
        mod = MrpackIndexer(file_path)
    else:
        mod = ModIndexer(file_path)
else:
    mb.showerror(title=f"MoDpack file not found",
                 message="A path to a modpack file has not been supplied (E1)")
    root.destroy()
    exit()


# Geometry and window size
weight, height = 400, 200

root.title("Mod Installer")
try:
    root.iconbitmap("C:/Program Files (x86)/ModInstaller/icon.ico")
except TclError:
    print("Icon not definned")
# root.maxsize(weight, height)
# root.minsize(weight, height)
root.geometry(f"{weight}x{height}")

# Variables
gui_name = StringVar()
gui_desc = StringVar()
gui_path = StringVar()

# GUI elements
text_write = ttk.Entry(root, width=50, textvariable=gui_path)
title = Label(root, textvariable=gui_name, font=("Console", 24))
desc = Label(root, textvariable=gui_desc, font=("Console", 10))
path_text = Label(root, text="Current directory:", font=("Console", 8))
mod_info = Label(root, text=f"{mod.version} | {mod.mod_count} mods", font=("Console", 10))

change_dir = Button(root, text="browse", command=browse_button)
install = Button(root, text="install", command=install, width=10, )
cancel = Button(root, text="cancel", width=10, command=destroy)

# Setting variables
gui_name.set(mod.name)
gui_desc.set(mod.description)

data = json_read(app_directory + "data.json")
gui_path.set(data["default_directory"])

title.place(relx=0.5, rely=0.1, anchor="center")
desc.place(relx=0.5, rely=0.25, anchor="center")

path_text.place(relx=0, rely=0.38, anchor="w")
change_dir.place(relx=0.83, rely=0.5, anchor="w")

mod_info.place(relx=0.5, rely=0.675, anchor="center")

install.place(relx=0.65, rely=0.85, anchor="center")
cancel.place(relx=0.35, rely=0.85, anchor="center")

text_write.place(relx=0.8, rely=0.5, anchor="e")

root.mainloop()

if progress:
    win2 = Tk()
else:
    exit()

# Geometry and window size
weight, height = 500, 200

win2.title("Mod Installer")
try:
    win2.iconbitmap("C:/Program Files (x86)/ModInstaller/icon.ico")
except TclError:
    print("Icon not definned")

# win2.maxsize(weight, height)
# win2.minsize(weight, height)
win2.geometry(f"{weight}x{height}")

current_mod = StringVar()

title2 = Label(win2, text="Installing Pack...", font=("Console", 25))
mod_label = Label(win2, textvariable=current_mod)
warning = Label(win2, text="Please DO NOT CLOSE this window")

title2.pack()
warning.pack()

progress_var = tk.DoubleVar()

progress_bar = ttk.Progressbar(win2, variable=progress_var, orient=HORIZONTAL, length=250, mode="determinate")

progress_bar.pack(pady=40)

mod_label.pack()

mod_path = gui_path.get()


def installer(progress_var):
    global response
    mod_dir = mod_path + f"\\{mod.mod_id}"
    print("Mod_dir:", mod_dir)

    # checking if user has the required version

    installed_versions = os.listdir(installed_versions_path)
    print(installed_versions)
    if mod.loader not in installed_versions:
        mb.showerror(title=f"{mod.loader} is not installed",
                     message="Please install it and try again")
        win2.destroy()
    else:
        print(f"{mod.loader} installed, continuing")
    try:
        os.mkdir(mod_dir)
        os.mkdir(mod_dir + "\\mods")
    except FileExistsError:
        mb.showerror(title="Modpack already installer",
                     message="It appears that this modpack has already been installed")
        win2.destroy()

    chunk_size = 8192
    progress_per_mod = 100 // mod.mod_count

    for i, (name, link) in enumerate(mod.mods_dir.items()):

        try:
            response = requests.head(link)
        except:
            mb.showerror(title="Connection Error",
                         message="Something went wrong while trying to download the mods, Check your internet "
                                 "connection then try again later...")
            import shutil

            shutil.rmtree(mod_dir)
            win2.destroy()

        file_size = int(response.headers.get('Content-Length'))
        chunk_n = file_size // chunk_size
        try:
            progress_per_chunk = round(progress_per_mod / chunk_n, 5)
        except:
            print("er")
        print(f"Dowloading mod: {name}, {i + 1}/{mod.mod_count}, from: {link}")
        current_mod.set(f"Downloading {name}...")
        with requests.get(link, stream=True) as response:
            # response.raise_for_status()
            with open(mod_dir + f"\\mods\\{name}", 'wb') as f:
                for j, chunk in enumerate(response.iter_content(chunk_size=chunk_size)):
                    if chunk:  # Filter out keep-alive new chunks
                        f.write(chunk)
                        progress_var.set(progress_var.get() + progress_per_chunk)

    print("Downloading complete")

    current_mod.set(f"Creating profile...")

    print("Creating profile")

    # ADD VERSION CHECK!!!!

    launcher_profile_data = json_read(launcher_profiles)

    mod_profile = {"icon": "Grass", "gameDir": mod_dir, "lastVersionId": mod.loader, "name": mod.name,
                   "type": "custom"}

    profile = launcher_profile_data["profiles"]
    profile[mod.mod_id] = mod_profile
    json_write(launcher_profile_data, launcher_profiles)

    print("Pofile created successfully")
    print("Saving")

    mmi_mod_profile = {"name": mod.name, "desc": mod.description, "version": mod.version, "mods": mod.mod_count}

    mmi_mod_profile_data = json_read(app_directory + "data.json")
    packs = mmi_mod_profile_data['packs']
    packs[mod.mod_id] = mmi_mod_profile
    json_write(mmi_mod_profile_data, app_directory + "data.json")

    progress_var.set(f"Installation Complete")

    mb.showinfo(title="Installation complete", message=f"{mod.name} has been successfully installed!")
    win2.destroy()


installer_thread = threading.Thread(target=installer, args=(progress_var,), daemon=True)
installer_thread.start()

win2.mainloop()
