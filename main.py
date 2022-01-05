import pynput
import keyboard
import json
import tkinter
import threading

from tkinter import filedialog
from tkinter import messagebox
from macro_parser import parse_file


PROGRAM_NAME = "Macro Everything"
VERSION = "0.1"


def parse_config():
    with open("config.json", "r") as file:
        data = json.load(file)
    return data


def get_hotkeys_dict(conf):
    ret = dict()
    ret[conf["emergency_stop"]] = stop
    ret[conf["start_last"]] = start_last
    ret[conf["restart_last"]] = restart_last
    ret[conf["stop_macro"]] = stop_macro
    ret[conf["toggle_recording"]] = toggle_record
    ret[conf["choose_macro"]] = select_macro

    return ret


def stop():
    print("Iterrupted!")
    quit()


def start_last():
    print("starting last used macro")


def restart_last():
    print("restarting macro")


def stop_macro():
    print("Stopping current macro")


def select_macro():
    # Not implemented
    print("Selection Dialog")
    root = tkinter.Tk()
    root.withdraw()
    file_path = tkinter.filedialog.askopenfilename(initialdir=BASE_PATH, title="Select Macro", multiple=False)
    root.destroy()

    if not file_path.endswith(".macro"):
        alert("Bad file!", "You have to select a .macro file!")
    else:
        parse_file(file_path)


def toggle_record():
    # Not implemented!
    print("starting to record macro")


def alert(title, msg):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showerror(title=title, message=msg)
    root.destroy()


class HelpWindow(threading.Thread):
    def __init__(self, conf):
        super().__init__()
        self.conf = conf

    def run(self):
        root = tkinter.Tk()
        root.title(f"{PROGRAM_NAME} - v{VERSION}")
        root.configure(background="white")
        root.grid_rowconfigure(10, weight=1)
        for i, x in enumerate(self.conf):
            if x == "last_used":
                break
            a = tkinter.Label(root, text=x, bg="white")
            a.config(font=("Calibri", 14, "bold"))
            a.grid(row=i, column=0)

            b = tkinter.Label(root, text=self.conf[x], bg="white")
            b.config(font=("Calibri", 14, "bold"))
            b.grid(row=i, column=2, padx=10)

        root.mainloop()


config = parse_config()

BASE_PATH = config["base_path"]

help_window = HelpWindow(config)
help_window.daemon = True
help_window.start()

with pynput.keyboard.GlobalHotKeys(get_hotkeys_dict(config)) as hotkeys:
    hotkeys.join()
