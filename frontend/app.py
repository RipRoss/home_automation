from flask import Flask, render_template


app_name = "alarm_frontend"


def create_app():
    return Flask(__name__)


app = create_app()


@app.route('/', methods=['GET'])
def display_alarm():
    return render_template('alarm.html')
