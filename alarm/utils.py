from alarm import config
import requests
import json


def toggle_alarm(state):
    if is_alarm_enabled(state):
        disable_alarm()
        return
    enable_alarm()


def enable_alarm():
    headers = {
        "Authorization": f"Bearer {config.alarm_config['api_key']}",
        "Content-Type": "application/json"
    }

    payload = {
        "state": "on"
    }

    try:
        requests.post(f"http://{config.alarm_config['host']}:{config.alarm_config['port']}/api/states/"
                             f"{config.alarm_config['alarm_entity_id']}", headers=headers, data=json.dumps(payload))
    finally:
        return


def disable_alarm():
    headers = {
        "Authorization": f"Bearer {config.alarm_config['api_key']}",
        "Content-Type": "application/json"
    }

    payload = {
        "state": "off"
    }

    try:
        requests.post(f"http://{config.alarm_config['host']}:{config.alarm_config['port']}/api/states/"
                      f"{config.alarm_config['alarm_entity_id']}", headers=headers, data=json.dumps(payload))
    finally:
        return


def is_alarm_enabled(state):
    if state == "on":
        return True
    return False


def confirm_pin(pin):
    if pin == "8839":
        return True
    return False


def confirm_state():
    headers = {
        "Authorization": f"Bearer {config.alarm_config['api_key']}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.get(f"http://{config.alarm_config['host']}:{config.alarm_config['port']}/api/states/"
                            f"{config.alarm_config['alarm_entity_id']}", headers=headers)
        data = resp.json()
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("error")
        return
        #raise e
    return data["state"]


def confirm_state_change(old_state):
    i = 0
    while i < 2:
        new_state = confirm_state()
        i += 1
        if old_state != new_state:
            return True
    return False
