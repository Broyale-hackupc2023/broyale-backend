import os

from dotenv import load_dotenv
from flask import Flask, request, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from character import Character
from dungeon_master import DungeonMaster, Input

from user import User
from room import Room


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
socketio = SocketIO(app, cors_allowed_origins='*')

users = {}
rooms = {}

@socketio.on('connect')
def handle_connect():
    # Save the user's session ID
    session_id = request.sid
    print('Client connected:', session_id)


@socketio.on('disconnect')
def handle_disconnect():
    # Remove the user from the dictionary when they disconnect
    session_id = request.sid
    msg = f"Client disconnected: {session_id}"
    if session_id in users:
        msg += f" ({users[session_id]})"
        user = users[session_id]
        if user.room is not None:
            user.room.leave(user)
            send_rooms_update()
        del users[session_id]
    print(msg)


@socketio.on('login')
def handle_login(data):
    # Save the user's name and send them a list of rooms
    name = data['name']
    new_user = User(request.sid, name)
    users[new_user.sid] = new_user
    send_rooms_update(new_user)
    print('New user:', name)


@socketio.on('create_room')
def handle_create_room(data):
    # Save the room and send an update to all users
    name = data['name']
    description = data['description']
    owner = users[request.sid]
    room_id = len(rooms)
    while room_id in rooms:
        room_id += 1
    new_room = Room(room_id, name, description, owner)
    rooms[room_id] = new_room
    send_rooms_update()
    print('New room:', name)


@socketio.on('join_room')
def handle_join_room(data):
    # Join the room and send an update to all users
    room_id = data['room_id']
    room = rooms[room_id]
    user = users[request.sid]
    user.join(room)
    send_rooms_update()
    print(user, 'joined', room)


@socketio.on('leave_room')
def handle_leave_room():
    # Leave the room and send an update to all users
    user = users[request.sid]
    user.leave_room()
    send_rooms_update()
    print(user, 'left the room')





def send_rooms_update(user=None):
    # Sends a list of rooms all users
    # If a user is specified, only send the list to that user
    rooms_list = []
    for room in rooms.values():
        rooms_list.append(room.to_dict())
    event = 'rooms_update'

    print("USERS LIST: ", users)
    if user is None:
        for user in users.values():
            emit(event, rooms_list, room=user.sid) 
    else:
        emit(event, rooms_list, room=user.sid)
        



if __name__ == '__main__':
	host = os.getenv('HOST')
	port = int(os.getenv('PORT'))

	print(f'Starting server on {host}:{port}')
	socketio.run(app, host=host, port=port)
