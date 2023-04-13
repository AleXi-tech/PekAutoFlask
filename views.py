# views.py
import os
import sys
import json
from flask import Blueprint, render_template, jsonify

views = Blueprint(__name__, "views")

def get_data_file_path():
    if getattr(sys, 'frozen', False):
        # Running in a bundled executable (pyinstaller)
        base_path = sys._MEIPASS
    else:
        # Running in normal Python environment
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "messages.json")

def load_messages():
    messages_path = get_data_file_path()
    try:
        with open(messages_path, "r") as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = []
    return messages

def save_messages(messages):
    messages_path = get_data_file_path()
    with open(messages_path, "w") as f:
        json.dump(messages, f)

@views.route("/")
def display_messages():
    messages = load_messages()
    print(f"Passing {len(messages)} messages to the template.")
    return render_template("messages.html", messages=messages)

@views.route("/messages/json")
def messages_json():
    messages = load_messages()
    return jsonify(messages)

@views.route("/messages/clear", methods=["POST"])
def clear_messages():
    save_messages([])
    return jsonify({"success": True})