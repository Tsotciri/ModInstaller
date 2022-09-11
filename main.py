from utils.internet import large_download
from utils.console import panel
from utils.console import markdown
from utils.console import table
from utils.ui import file_window
from utils.console import close
from rich import print
from installer import install
from installer import uninstall
import time
import os
import json

user = os.getlogin()

if not os.name == "nt":
    print("[red]Sorry but only Windows is supported :([/red]\nYou can contribute over at GitHub :) -> https://github.com/Tsotciri/ModInstaller")
    time.sleep(2)
    print("Press Enter to continue:")
    input("")
    close()
else:
    print("")

app_directory = f"C:\\Users\\{user}\\AppData\\Roaming\\.mod-installer\\"

if not os.path.exists(app_directory + ".installed"):
    install()
    
with open(app_directory + "data.json", "r") as f:
        json_data = json.load(f)
if json_data['version'] < 0.2:
    print("Updating...")
    time.sleep(3)
    with open(app_directory + "data.json", "w") as f:
        json_data['version'] = 0.2
        json.dump(json_data,f, indent=2)


title = """
[cyan]
                                                     [bold]Minecraft[/bold]
 /$$      /$$                 /$$       /$$$$$$                       /$$               /$$ /$$                    
| $$$    /$$$                | $$      |_  $$_/                      | $$              | $$| $$                    
| $$$$  /$$$$  /$$$$$$   /$$$$$$$        | $$   /$$$$$$$   /$$$$$$$ /$$$$$$    /$$$$$$ | $$| $$  /$$$$$$   /$$$$$$ 
| $$ $$/$$ $$ /$$__  $$ /$$__  $$        | $$  | $$__  $$ /$$_____/|_  $$_/   |____  $$| $$| $$ /$$__  $$ /$$__  $$
| $$  $$$| $$| $$  \ $$| $$  | $$        | $$  | $$  \ $$|  $$$$$$   | $$      /$$$$$$$| $$| $$| $$$$$$$$| $$  \__/
| $$\  $ | $$| $$  | $$| $$  | $$        | $$  | $$  | $$ \____  $$  | $$ /$$ /$$__  $$| $$| $$| $$_____/| $$      
| $$ \/  | $$|  $$$$$$/|  $$$$$$$       /$$$$$$| $$  | $$ /$$$$$$$/  |  $$$$/|  $$$$$$$| $$| $$|  $$$$$$$| $$      
|__/     |__/ \______/  \_______/      |______/|__/  |__/|_______/    \___/   \_______/|__/|__/ \_______/|__/
                                                                                                         by Tsotciri[/cyan]
"""

print(title)

panel("v0.2")
print("")

print("[white bold]Please choose what you want to do for the below choices:[/white bold]")

table(["Install Mods", "Help", "Exit"])

while True:
    choice = input(">").upper()
    if choice == "HELP":
        print("Selected: [green]Help")
        time.sleep(2)
        print('''
        +---------------------------------------------------------------------------------------------------------------------+
        |- Mod Installer is an application made to automatically download and install mods for the game Minecraft             |
        | [bold](This Application has nothing to do with Mojang, this is a third-party application)[/bold]                                 |
        |- Mod Installer works by reading data from a simple text file, these files contain the version of the client and     |                                                                                     
        | links to download the mods, when you select this file Mod Installer reads the data and starts downloading the mods  |                                                                                      
        | to the AppData directory and then creates a client in the minecraft launcher!                                       |                                                                                      
        |- Currently the links to the mods are dropbox links from my dropbox :)                                               |
        |- Feel free to contribute or report bugs over at the GiHub                                            |
        |- TIP: To uninstall Mod Installer and wipe all of its data type Uninstall (use with caution)                         |                                                                                      
        +---------------------------------------------------------------------------------------------------------------------+
        ''')
        time.sleep(3)
    elif choice == "EXIT":
        close()
    elif choice == "INSTALL MODS":
        print("Selected: [green]Install Mods[/green]")
        break
    elif choice == "UNINSTALL":
        uninstall()
    else:
        print("[red]Incorrect choice, please try again...[/red]")

markdown("### Please select a MI file\n")

file = file_window("Please select a MI file", True)

file_data = []

for mod in file:
    file_data.append(mod.replace("\n", ""))

if file_data[0] != "MIfile":
    print("[red]Selected file is not compatible")
    print("Press Enter to continue:")
    input("")
    close()
else:
    print("[green]Selected file is compatible!")
print("")
modpack_version = file_data[1]
modpack_name = file_data[2]
modpack_id = file_data[3]
modpack_desc = file_data[4]
modpack_mods = file_data[5:]
modpack_mods_count = len(modpack_mods)

time.sleep(1)

with open(app_directory + "data.json", "r") as f:
    modpacks = json.load(f)
    installed_modpacks = modpacks['packs']

    if modpack_id in installed_modpacks:
        print("[red]You have already installed that modpack")
        print("Press Enter to continue:")
        input("")
        close()
    else:
        print("")

versions = []

for version_name in os.listdir(f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\versions"):
    versions.append(version_name)

markdown("### Do you want to install this modpack?")
print(f"Name: {modpack_name}")
print(f"Description: {modpack_desc}")
print(f"Mods: {modpack_mods_count}")
print(f"Version: {modpack_version}")
print("")

choice = input("Do you want to continue? (yes/no)> ")
if choice.upper() != "YES":
            if choice.upper() == "NO":
                close()
            print("[red]I didn't understand that...")
            close()
else:
    pass

if modpack_version in versions:
    print("[green]Modloader already Installed!")
else:
    print(f"[red]You don't have the version {modpack_version} installed please install it and run the installer again...")
    print("Press Enter to continue:")
    input("")
    close()

modpack_dir = app_directory + f"clients\\{modpack_id}"

os.mkdir(modpack_dir)
os.mkdir(modpack_dir + "\\mods")

count = 1
for links in modpack_mods:
    large_download(links, app_directory + f"clients\\{modpack_id}\\mods\\mod-{count}.jar", f"downloading mods ({count}/{modpack_mods_count}): ")
    count += 1
print("[green]Succesfully downloaded mods")
time.sleep(1)

launcher_profiles = f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\launcher_profiles.json"

print("[green]Creating profile...")
with open(launcher_profiles) as f:
    lp_data = json.load(f)

modpack_profile =  {"icon" : "Grass", "gameDir": modpack_dir , "lastVersionId" : modpack_version, "name" : modpack_name, "type" : "custom"}

with open(launcher_profiles, "w") as f:
    profile = lp_data['profiles']
    profile[modpack_id] = modpack_profile
    json.dump(lp_data,f, indent=2)

modpack_data_default = {"name": modpack_name,"desc": modpack_desc,"version": modpack_version,"mods": modpack_mods_count}

with open(app_directory + "data.json") as f:
    modpack_data = json.load(f)

with open(app_directory + "data.json", "w") as f:
    packs = modpack_data['packs']
    packs[modpack_id] = modpack_data_default
    json.dump(modpack_data, f, indent=2)

time.sleep(2)
print(f"[bold green]Succesfully Installed {modpack_name}!")
time.sleep(1)
print("Press Enter to continue:")
input("")
close()