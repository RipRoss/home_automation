from flask import Flask, request, Response
from alarm import utils

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

    if not utils.confirm_pin(pin):
        return Response("{'message': 'Incorrect PIN'}", status=401, mimetype="application/json")

    state = utils.confirm_state()

    utils.toggle_alarm(state)

    state_changed = utils.confirm_state_change(state)

    if state_changed:
        return {"status": "success"}
    return Response("{'status': 'failed'}", status=401, mimetype="application/json")


def _validate_request(payload):
    if not payload or "pin" not in payload:
        return False
    return True

