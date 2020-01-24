from flask import Flask, request, Response, jsonify
import requests
from alarm import config
import json

app_name = "alarm_wsapi"


def create_app():
    return Flask(__name__)


app = create_app()


@app.route('/confirm', methods=['POST'])
def confirm_pin():
    confirmation = request.get_json()

    if not _validate_request(confirmation):
        return Response("{'message':'Incorrect JSON payload'}", status=400, mimetype="application/json")

    pin = confirmation["pin"]

    if not _confirm_pin(pin):
        return Response("{'message': 'Incorrect PIN'}", status=401, mimetype="application/json")

    state = _confirm_state()

    _toggle_alarm(state)

    state_changed = _confirm_state_change(state)

    if state_changed:
        return {"status": "success", "new_state": state}
    return Response("'status': 'failed', 'new_state': {state}, 'message': 'Check home assistance instance for "
                    "availability'}".format(state=state))


def _confirm_state_change(old_state):
    i = 0
    while i < 5:
        new_state = _confirm_state()
        if old_state != new_state:
            return True
    return False


def _confirm_state():
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
        #raise e
    return data["state"]


def _toggle_alarm(state):
    if _is_alarm_enabled(state):
        _disable_alarm()
        return
    _enable_alarm()


def _enable_alarm():
    headers = {
        "Authorization": f"Bearer {config.alarm_config['api_key']}",
        "Content-Type": "application/json"
    }

    payload = {
        "state": "on"
    }

    try:
        resp = requests.post(f"http://{config.alarm_config['host']}:{config.alarm_config['port']}/api/states/"
                             f"{config.alarm_config['alarm_entity_id']}", headers=headers, data=json.dumps(payload))
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise e


def _disable_alarm():
    headers = {
        "Authorization": f"Bearer {config.alarm_config['api_key']}",
        "Content-Type": "application/json"
    }

    payload = {
        "state": "off"
    }

    try:
        resp = requests.post(f"http://{config.alarm_config['host']}:{config.alarm_config['port']}/api/states/"
                             f"{config.alarm_config['alarm_entity_id']}", headers=headers, data=json.dumps(payload))
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise e


def _is_alarm_enabled(state):
    if state == "on":
        return True
    return False


def _confirm_pin(pin):
    if pin == "8839":
        return True
    return False


def _validate_request(payload):
    if not payload or "pin" not in payload:
        return False
    return True

