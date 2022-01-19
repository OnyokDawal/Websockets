from flask import Flask, render_template, request, redirect, url_for, session;
from flask_socketio import SocketIO, send, join_room, leave_room, emit;

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecret"
io = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'
clients = []

@io.on('connect')
def handle_connect():
    print('Client connected')
    clients.append(request.sid)

@io.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    clients.remove(request.sid)
@io.on('message')
def send_message(client_id, data):
    send('output', data, room=client_id)
    print('sending message "{}" to client "{}".'.format(data, client_id))

#Broadcast message
# @io.on('message')
# def handleMessage(msg):
#     send(msg, broadcast=True)
#     return None


# @io.on('join')
# def on_join(data):
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     send(username + ' has entered the room.', to=room)

# @io.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room.', to=room)

# @io.on("join")
# def join(message):
#     clients.append(request.sid)
#     room = session.get('room')
#     join_room(room)
#     emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=sid)


if __name__ == '__main__':
    io.run(app)