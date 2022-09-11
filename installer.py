from utils.console import close
from rich import print
import subprocess
import shutil
import json
import time
import os

user = os.getlogin()

app_directory = f"C:\\Users\\{user}\\AppData\\Roaming\\.mod-installer\\"

def install():
    print("Performing first time setup...")
    time.sleep(3)
    os.mkdir(app_directory)
    os.mkdir(app_directory + "clients")
    open(app_directory + ".installed", "x")
    open(app_directory + "data.json", "x")
    print("[green]Successfully installed ModInstaller")

    default_json_data = {"version": 0.2,"packs": {}}

    with open(app_directory + "data.json", "w") as f:
        json.dump(default_json_data,f, indent=2)

def uninstall():

    uninstall_exe = "C:\\Program Files (x86)\\ModInstaller\\unins000.exe"

    warning = '''[bold red]
 __          __              _             _ 
 \ \        / /             (_)           | |
  \ \  /\  / /_ _ _ __ _ __  _ _ __   __ _| |
   \ \/  \/ / _` | '__| '_ \| | '_ \ / _` | |
    \  /\  / (_| | |  | | | | | | | | (_| |_|
     \/  \/ \__,_|_|  |_| |_|_|_| |_|\__, (_)
                                      __/ |  
                                     |___/   
    '''
    print(warning)
    time.sleep(2)
    print("[red]Are you sure you want to [bold]wipe Mod Inatller data and uninstall it[/bold], that includes minecraft clients that you installed using Mod Installer!")
    print("[bold red]This is can not be undone!")
    print("")
    choice = input("Wipe all data and uninstall Mod Installer? (no/yes) > ")
    if choice.upper() == "YES":
        print("[red]Uninstalling...")
        time.sleep(1)

        print("[red]Deleting Profiles...")
        time.sleep(5)

        launcher_profiles_file = f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\launcher_profiles.json"

        with open(app_directory + "data.json", "r") as f:
            ap_data = json.load(f)
            modpack_profiles = ap_data['packs']

        with open(launcher_profiles_file, "r") as f:
            lp_data = json.load(f)
            launcher_profiles = lp_data['profiles']

        with open(launcher_profiles_file, "w") as f:
            for modpack in modpack_profiles:
                print(f"[red]Uninstalling: {modpack}")
                del launcher_profiles[modpack]
            json.dump(lp_data,f, indent=2)

        print("[red]Profiles Deleted")
        time.sleep(1)
        print("[red]Deleting files...")
        time.sleep(3)
        shutil.rmtree(app_directory)
        print("[red]Files Deleted")
        time.sleep(1)
        print("[red]Uninstalling Mod Installer")
        time.sleep(2)
        subprocess.call([uninstall_exe])
        close()
    else:
        print("[green]Uninstall cancelled")
        time.sleep(2)
        return "uninstalled cancelled"