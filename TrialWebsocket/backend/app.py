from flask import Flask, render_template, request, redirect, url_for, session;
from flask_socketio import SocketIO, send, join_room, leave_room, emit;

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecret"
app.config['DEBUG'] = True
io = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'
clients = []

# @io.on('connect')
# def handle_connect():
#     print('Client connected')
#     clients.append(request.sid)

# @io.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')
#     clients.remove(request.sid)
# @io.on('message')
# def send_message(client_id, data):
#     send('output', data, room=client_id)
#     print('sending message "{}" to client "{}".'.format(data, client_id))

@app.route('/')
def index():
    return render_template('index.html')

# Broadcast message
@io.on('message')
def handleMessage(msg):
    send(msg, broadcast=True)
    return None

@io.on('username', namespace='/private')
def receive_username(username):
    clients.append({username : request.sid})
    print(clients)

@io.on('message from user', namespace='/messages')
def receive_message_from_user(message):
    print('USER MESSAGE: {}'.format(message))
    emit('from flask', message.upper(), broadcast=True)

@app.route('/originate')
def originate():
    io.emit('server originated', 'Something happened on the server!')
    return '<h1>Sent!</h1>'

# #Exit room
# @io.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room.', to=room)

# @io.on("join")
# def join(message, sid):
#     clients.append(request.sid)
#     room = session.get('room')
#     join_room(room)
#     emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=sid)


if __name__ == '__main__':
    io.run(app)