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


#user = os.getlogin()
#app_directory = f"C:\\Users\\{user}\\AppData\\Roaming\\.mod-installer\\"
#install_path = app_directory + "clients"
#
#launcher_profiles = f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\launcher_profiles.json"
#installed_versions_path = f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\versions"
#
#file_path = r"C:\Users\Ktsotas\Downloads\Bouble Cum 1.0.3\modrinth.index.json"
#mod = MrpackIndexer(file_path)
#print(mod.name, mod.mod_id, mod.description, mod.mod_count)
#
#for i in mod.mods_dir:
#    print(mod.mods_dir[i])
#
#def json_read(file):
#    with open(file, "r") as f:
#        return json.load(f)
#
#
#def json_write(data, file):
#    with open(file, "w") as f:
#        json.dump(data, f, indent=2)
#        return True
#
#
#def install():
#    global progress
#    root.destroy()
#    progress = True
#
#
#def destroy():
#    root.destroy()
#    quit()
#
#
#def browse_button():
#    filename = filedialog.askdirectory()
#    if filename != "":
#        data = json_read(app_directory + "data.json")
#        data["default_directory"] = filename
#        json_write(data, app_directory + "data.json")
#        gui_path.set(filename)
#
## Root
#root = Tk()
#
#
## Geometry and window size
#weight, height = 400, 200
#
#root.title("Mod Installer")
#try:
#    root.iconbitmap("C:/Program Files (x86)/ModInstaller/icon.ico")
#except TclError:
#    print("Icon not definned")
## root.maxsize(weight, height)
## root.minsize(weight, height)
#root.geometry(f"{weight}x{height}")
#
## Variables
#gui_name = StringVar()
#gui_desc = StringVar()
#gui_path = StringVar()
#
## GUI elements
#text_write = ttk.Entry(root, width=50, textvariable=gui_path)
#title = Label(root, textvariable=gui_name, font=("Console", 24))
#desc = Label(root, textvariable=gui_desc, font=("Console", 10))
#path_text = Label(root, text="Current directory:", font=("Console", 8))
#mod_info = Label(root, text=f"{mod.version} | {mod.mod_count} mods", font=("Console", 10))
#
#change_dir = Button(root, text="browse", command=browse_button)
#install = Button(root, text="install", command=install, width=10, )
#cancel = Button(root, text="cancel", width=10, command=destroy)
#
## Setting variables
#gui_name.set(mod.name)
#gui_desc.set(mod.description)
#
#data = json_read(app_directory + "data.json")
#gui_path.set(data["default_directory"])
#
#title.place(relx=0.5, rely=0.1, anchor="center")
#desc.place(relx=0.5, rely=0.25, anchor="center")
#
#path_text.place(relx=0, rely=0.38, anchor="w")
#change_dir.place(relx=0.83, rely=0.5, anchor="w")
#
#mod_info.place(relx=0.5, rely=0.675, anchor="center")
#
#install.place(relx=0.65, rely=0.85, anchor="center")
#cancel.place(relx=0.35, rely=0.85, anchor="center")
#
#text_write.place(relx=0.8, rely=0.5, anchor="e")
#
#root.mainloop()
#