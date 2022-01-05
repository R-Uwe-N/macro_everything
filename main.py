import pynput
import keyboard
import json
import tkinter

from tkinter import filedialog
from tkinter import messagebox
from macro_parser import parse_file


def parse_config():
    with open("config.json", "r") as file:
        data = json.load(file)
    return data


def get_hotkeys_dict(conf):
    ret = dict()
    ret[conf["emergency_stop"]] = stop
    ret[conf["start_last"]] = start_last
    ret[conf["toggle_recording"]] = toggle_record
    ret[conf["choose_macro"]] = select_macro

    return ret


def stop():
    print("Iterrupted!")
    quit()


def start_last():
    print("starting last used macro")


def select_macro():
    # Not implemented
    print("Selection Dialog")
    root = tkinter.Tk()
    root.withdraw()
    file_path = tkinter.filedialog.askopenfilename(initialdir=BASE_PATH, title="Select Macro", multiple=False)
    root.destroy()

    if not file_path.endswith(".macro"):
        alert("Bad file!", "You have to select a .macro file!")

    parse_file(file_path)


def toggle_record():
    # Not implemented!
    print("starting to record macro")


def alert(title, msg):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showerror(title=title, message=msg)
    root.destroy()


config = parse_config()

BASE_PATH = config["base_path"]

with pynput.keyboard.GlobalHotKeys(get_hotkeys_dict(config)) as hotkeys:
    hotkeys.join()
