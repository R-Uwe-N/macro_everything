import pynput
import keyboard
import json
import tkinter
import threading
import os

from tkinter import filedialog
from tkinter import messagebox

import macro_parser
from macro_parser import parse_file


PROGRAM_NAME = "Macro Everything"
VERSION = "0.1"


def set_last_macro(path):
    data = parse_config()
    data["last_used"] = path
    write_config(data)


def get_last_macro():
    data = parse_config()
    return data["last_used"]


def parse_config():
    with open("config.json", "r") as file:
        data = json.load(file)
    return data


def write_config(data):
    with open("config.json", "w") as file:
        json.dump(data, file, indent=4)


def get_hotkeys_dict(conf):
    ret = dict()
    ret[conf["emergency_stop"]] = stop
    ret[conf["start_last"]] = start_last
    ret[conf["restart_last"]] = restart_last
    ret[conf["stop_macro"]] = stop_macro
    ret[conf["toggle_recording"]] = toggle_record
    ret[conf["choose_macro"]] = select_macro

    return ret


class HelpWindow(threading.Thread):
    def __init__(self, conf):
        super().__init__()
        self.conf = conf
        self.is_active = False
        self.active_label = None
        self.root = None

    def run(self):
        self.root = tkinter.Tk()
        self.root.title(f"{PROGRAM_NAME} - v{VERSION}")
        self.root.resizable(False, False)
        self.root.attributes("-toolwindow", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(background="white")
        self.root.grid_rowconfigure(10, weight=1)
        while True:
            for i, x in enumerate(self.conf):
                if x == "base_path":
                    break
                if x == "last_used":
                    a = tkinter.Label(self.root, text="Current Macro", bg="white")
                    self.active_label = tkinter.Label(self.root, text=os.path.basename(self.conf[x]),
                                                      bg=("green" if self.is_active else "red"))  # Display Active macro
                    self.active_label.config(font=("Calibri", 14, "bold"))
                    self.active_label.grid(row=i, column=2, padx=10)
                    b = self.active_label
                else:
                    a = tkinter.Label(self.root, text=x, bg="white")  # Display Hotkey name
                    b = tkinter.Label(self.root, text=self.conf[x], bg="white")  # Display Hotkey

                a.config(font=("Calibri", 14, "bold"))
                a.grid(row=i, column=0)
                b.config(font=("Calibri", 14, "bold"))
                b.grid(row=i, column=2, padx=10)

            self.root.update_idletasks()
            self.root.update()

    def active(self, boolean):
        self.is_active = boolean
        self.conf = parse_config()


config = parse_config()

BASE_PATH = config["base_path"]

help_window = HelpWindow(config)
help_window.daemon = True  # Daemon so it closes on program quit
help_window.start()


def stop():
    print("Iterrupted!")
    quit()


def start_last():
    macro = get_last_macro()
    if macro:
        help_window.active(True)
        macro_parser.parse_file(macro)
    else:
        alert("No Macro Selected!", "You have to select a Macro before Starting!")


def restart_last():
    help_window.active(False)
    print("restarting macro")
    help_window.active(True)


def stop_macro():
    help_window.active(False)
    print("Stopping current macro")


def select_macro():
    stop_macro()
    # Not implemented
    print("Selection Dialog")
    root = tkinter.Tk()
    root.withdraw()
    file_path = tkinter.filedialog.askopenfilename(parent=root, initialdir=BASE_PATH, title="Select Macro", multiple=False)

    root.destroy()

    if not file_path.endswith(".macro"):
        alert("Bad file!", "You have to select a .macro file!")
    else:
        set_last_macro(os.path.relpath(file_path))
        help_window.active(False)


def toggle_record():
    # Not implemented!
    print("starting to record macro")


def alert(title, msg):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showerror(parent=root, title=title, message=msg)
    root.mainloop()
    root.destroy()


with pynput.keyboard.GlobalHotKeys(get_hotkeys_dict(config)) as hotkeys:
    hotkeys.join()
