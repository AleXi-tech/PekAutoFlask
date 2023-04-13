# server.py
import os
import sys
import socket
import datetime
import json

HOST = ''
PORT = 8001

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

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print('Waiting for a connection...')

        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode('utf-8').strip('\n')
                    if not message:
                        continue
                    now = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")
                    message = {"date": now, "message": message}
                    print(message)

                    messages = load_messages()
                    messages.append(message)
                    save_messages(messages)
