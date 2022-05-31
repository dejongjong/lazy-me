import os
import sys

from flask import Flask, request

from actions import todoist

app = Flask(__name__)
print(sys.version)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/update-next-actions", methods=["POST"])
def update_next_actions():
    data = request.get_json()
    if data is None:
        return "Bad request: No POST data received", 400

    try:
        todoist.update_next_actions(
            token=data["token"], next_action_label=data.get("next_action_label")
        )
        return "Success", 204

    except KeyError:
        return "Bad request: No token provided", 400


if __name__ == "__main__":
    if os.environ.get("ENV") in ["production", "staging"]:
        app.run(host="0.0.0.0", port=int(os.environ["PORT"]))
    else:
        app.run(use_reloader=False, debug=True, port=5000)
