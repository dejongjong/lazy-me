import os
import sys

from flask import Flask, request

from actions import todoist

app = Flask(__name__)
print(sys.version)


@app.route("/")
def hello_world():
    return "Hello, World!", 200


@app.route("/update-next-actions", methods=["POST"])
def update_next_actions():
    data = request.get_json()
    if data is None:
        return "Bad Request: No POST data received", 400
    if not "token" in data:
        return "Bad Request: No token received", 400

    try:
        progress_messags = todoist.update_next_actions(
            token=data["token"], next_action_label=data.get("next_action_label")
        )
        return "\n".join(progress_messags), 204

    except Exception as err:
        return f"Internal Server Error: {str(err)}", 500


if __name__ == "__main__":
    if os.environ.get("ENV") in ["production", "staging"]:
        app.run(host="0.0.0.0", port=int(os.environ["PORT"]))
    else:
        app.run(use_reloader=False, debug=True, port=5000)
