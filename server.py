import os

from dotenv import load_dotenv
from flask import Flask, request, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
socketio = SocketIO(app, cors_allowed_origins='*')

users = {}


@socketio.on('connect')
def handle_connect():
    # Save the user's session ID
    session_id = request.sid
    users[session_id] = None
    print('Client connected:', session_id)


@socketio.on('disconnect')
def handle_disconnect():
    # Remove the user from the dictionary when they disconnect
    session_id = request.sid
    username = users[session_id]
    del users[session_id]
    print('Client disconnected:', session_id, username)


@socketio.on('message')
def handle_message(data):
    # Send the message to the recipient's personal room
    recipient = data['recipient']
    message = data['message']
    sender = users[request.sid]
    emit('message', {'sender': sender, 'message': message}, room=recipient)
    print('Message sent from', sender, 'to', recipient, ':', message)


if __name__ == '__main__':
	host = os.getenv('HOST')
	port = int(os.getenv('PORT'))

	print(f'Starting server on {host}:{port}')
	socketio.run(app, host=host, port=port)
