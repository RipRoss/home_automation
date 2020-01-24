import json


def get_config(filename):
    with open(f'config/{filename}', "r") as jfile:
        data = json.load(jfile)

    print(data)
    return data


alarm_config = get_config('config.json')