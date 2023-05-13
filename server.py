import os

from dotenv import load_dotenv
from flask import Flask, request, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from character import Character
from dungeon_master import DungeonMaster, Input

from user import User
from room import Room

from colorama import Fore, Back, Style


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
    print_state()


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
    print_state()

@socketio.on('login')
def handle_login(data):
    # Save the user's name and send them a list of rooms
    name = data['name']
    new_user = User(request.sid, name)
    users[new_user.sid] = new_user
    send_rooms_update(new_user)
    print('New user:', name)
    print_state()


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
    owner.join(new_room)
    send_rooms_update()
    emit('joined_room', new_room.to_dict(), room=owner.sid)
    print('New room:', name)
    print_state()


@socketio.on('join_room')
def handle_join_room(data):
    # Join the room and send an update to all users
    room_id = data['room_id']
    room = rooms[room_id]
    user = users[request.sid]
    user.join(room)
    send_rooms_update()
    emit('joined_room', room.to_dict(), room=user.sid)
    print(user, 'joined', room)
    print_state()


@socketio.on('leave_room')
def handle_leave_room():
    # Leave the room and send an update to all users
    user = users[request.sid]
    room = user.room
    if room is None:
        send_error('You are not in a room', user.sid)
        return

    user.leave_room()
    if len(room.users) == 0:
        del rooms[room.id]
    elif room.owner == user:
        room.owner = room.users[0]
    send_rooms_update()
    emit('joined_room', room.to_dict(), room=user.sid)
    print(user, 'left the room')
    print_state()


@socketio.on('start_game')
def handle_start_game(data):
    # Start the game and send an update to all users
    user = users[request.sid]
    room_id = data['room_id']
    room = rooms[room_id]

    if user != room.owner:
        send_error('Only the owner can start the game', user.sid)
        return
    
    if len(room.users) < 2:
        send_error('You need at least 2 characters to start the game', user.sid)
        return

    if user not in room.users or user.room != room:
        send_error('You must be in the room to start the game', user.sid)
        return
    
    room.start_game()
    send_rooms_update()
    print(user, 'started the game')
    print_state()






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

    print_state()


def send_error(error_message, sid):
    # Sends an error message to a user
    emit('error', error_message, room=sid)
    print_state()
        


def print_state():
    print(f"{Fore.LIGHTWHITE_EX}Users:{Style.RESET_ALL}")
    for user in users.values():
        if user.room:
            print(f"  {Fore.GREEN}{user.name}{Style.RESET_ALL} in {Fore.BLUE}{user.room.name}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}{user.name}{Style.RESET_ALL} not in a room")
    print()
    print(f"{Fore.LIGHTWHITE_EX}Rooms:{Style.RESET_ALL}")
    for room in rooms.values():
        print(f"  {Fore.BLUE}{room.name}{Style.RESET_ALL} ({len(room.users)} users)")
        for user in room.users:
            print(f"    {Fore.GREEN}{user.name}{Style.RESET_ALL}")
    print()




if __name__ == '__main__':
	host = os.getenv('HOST')
	port = int(os.getenv('PORT'))

	print(f'Starting server on {host}:{port}')
	socketio.run(app, host=host, port=port)
