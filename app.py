# app.py
import os
import sys
from flask import Flask, request
from views import views
from threading import Thread
from server import run_server
import webbrowser
import platform
import subprocess

def rule_exists(rule_name):
    try:
        result = subprocess.run(f'netsh advfirewall firewall show rule name="{rule_name}"', stdout=subprocess.PIPE, shell=True, text=True)
        return rule_name in result.stdout
    except subprocess.CalledProcessError as e:
        print(f'Error checking for existing firewall rule: {e}')
        return False

def add_firewall_rule_windows(rule_name, description):
    if rule_exists(rule_name):
        print(f'Firewall rule "{rule_name}" already exists. Skipping rule creation.')
        return

    try:
        command = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol=icmpv4:8,any interfacetype=any edge=yes profile=any enable=yes description="{description}"'
        subprocess.run(command, shell=True, check=True)
        print(f'Successfully added firewall rule: {rule_name}')
    except subprocess.CalledProcessError as e:
        print(f'Error adding firewall rule: {e}')

rule_name = 'ICMPv4 Echo Request'
description = 'Allow ICMPv4 Echo Request (ping)'

current_platform = platform.system()

if current_platform == 'Windows':
    add_firewall_rule_windows(rule_name, description)
else:
    print(f'{current_platform} is not supported.')



if getattr(sys, 'frozen', False):
    # Running in a bundled executable (pyinstaller)
    template_folder = os.path.join(sys._MEIPASS, "templates")
    static_folder = os.path.join(sys._MEIPASS, "static")
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # Running in normal Python environment
    app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

def run_flask_app():
    url = 'http://localhost:8080/'
    webbrowser.open(url)
    app.run(debug=True, use_reloader=False, port=8080)

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask_app)
    socket_thread = Thread(target=run_server)

    flask_thread.start()
    socket_thread.start()

    flask_thread.join()
    socket_thread.join()
