import pynput
import keyboard
import json


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


def toggle_record():
    # Not implemented!
    print("starting to record macro")


config = parse_config()

with pynput.keyboard.GlobalHotKeys(get_hotkeys_dict(config)) as hotkeys:
    hotkeys.join()
