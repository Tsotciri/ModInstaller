import os
import time
import datetime
from rich.console import Console
from rich.markdown import Markdown
from rich import print
from rich.panel import Panel
from rich.columns import Columns

console = Console()


# This is a function used to easly make a markdown text
def markdown(text):
    console.print(Markdown(text))


def table(items):
    console.print(Columns([Panel(f"[cyan]{item}", expand=True) for item in items]))


# This is a function used to easly make a panel
def panel(text, title="", subtitle=""):
    print(Panel(text, title=title, subtitle=subtitle))


# This is a function used to easly make a panel with the fit() function
def fit_panel(text, title="", subtitle=""):
    print(Panel.fit(text, title=title, subtitle=subtitle))


def close():
    print("[bold red]Closing...[/bold red]")
    time.sleep(1)
    exit()


def log(type, server, command="", players=4):
    date = datetime.datetime.now()
    if os.path.isfile("log.txt"):
        # log_file = open("log.txt", "a")
        print()
    else:
        # amogus = open("log.txt", "x")
        # amogus.close()
        # log_file = open("log.txt", "a")
        print()
    if type == "com":
        print(
            f'[blue][{date.strftime("%a")} {date.strftime("%d")} - {date.strftime("%H")}:{date.strftime("%M")}:{date.strftime("%S")}][/blue]',
            f"Command {command} was run in server {server}")
        # log_file.write(F'\n[{date.strftime("%a")} {date.strftime("%d")} - {date.strftime("%H")}:{date.strftime("%M")}:{date.strftime("%S")}] Command {command} was run in server {server}')
    elif type == "game":
        print(
            f'[blue][{date.strftime("%a")} {date.strftime("%d")} - {date.strftime("%H")}:{date.strftime("%M")}:{date.strftime("%S")}][/blue]',
            f'A game of palermo with {players} players is staring in server {server}')
        # log_file.write(F'\n[{date.strftime("%a")} {date.strftime("%d")} - {date.strftime("%H")}:{date.strftime("%M")}:{date.strftime("%S")}] A game of palermo with {players} players is staring in server {server}')
    # log_file.close()
