import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


def get_rate():
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f).get("dollar_rate", 0)
    except:
        return 0


def set_rate(new_rate):
    data = {}

    try:
        with open(CONFIG_PATH) as f:
            data = json.load(f)
    except:
        pass

    data["dollar_rate"] = new_rate

    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f)