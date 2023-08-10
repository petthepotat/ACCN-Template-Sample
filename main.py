from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
PORT = 5000

app = Flask(__name__)
app.config['SECRET'] = "secret123"
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def home_page():
  page = render_template('index.html')
  split = 'ip_address">'
  l, r = page.split(split)
  l += split + IPAddr + r
  return l


@socketio.on('connect')
def handle_message():
  print(f"Login Accepted")
  send(f"IP||{IPAddr}", broadcast=False)


@socketio.on('message')
def handle_message(message):
  if message.startswith("#UC#"):
    send(f"`{message[4:]}` joined the server||", broadcast=True)
    return
  # split message
  name, msg = message.split("||")
  print(f"{name}||{msg}")
  send(f"{name}||{msg}", broadcast=True)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=PORT, debug=True)
