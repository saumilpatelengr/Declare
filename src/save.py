import os
import sys
import json

def get_save_path():
    if sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support/Declare")
    else:
        base = os.path.join(os.path.expanduser("~"), ".declare")

    os.makedirs(base, exist_ok = True)
    return os.path.join(base, "save.json")


def load_save():
    path = get_save_path()

    if not os.path.exists(path):
        return {}

    with open(path, "r") as f:
        return json.load(f)


def write_value(key, value):
    data = load_save()
    data[key] = value

    with open(get_save_path(), "w") as f:
        json.dump(data, f)


def read_value(key, default=None):
    data = load_save()
    return data.get(key, default)