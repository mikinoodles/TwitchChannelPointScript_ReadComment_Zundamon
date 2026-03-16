import json
import sys
from pathlib import Path


def get_app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def get_config_as_dict() -> dict:
    config_file_path = get_app_dir() / "settings/config.json"

    data_dict: dict = {}

    with open(config_file_path, mode="r", encoding="utf8") as file:
        data_dict = json.load(file)

    return data_dict


def get_ng_word_list() -> list:
    ng_word_list_path = get_app_dir() / "settings/ng_word_list.txt"

    ng_word_list: list = []

    with open(ng_word_list_path, mode="r", encoding="utf8") as file:
        for line in file:
            stripped_line: str = line.strip()
            if stripped_line:
                ng_word_list.append(stripped_line)

    return ng_word_list



def __main__():
    config_dict = get_config_as_dict()

    print(config_dict)

if __name__ == "__main__":
    __main__()