from flask import Flask , render_template, request, jsonify
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import os 
import sqlite3


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") # Enabling websockets

DATABASE = 'mydatabase.db'
def get_users():
    """Fetch users from the mydatabase"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, profession FROM users")
    users = [{"username": row[0],"profession": row[1]} for row in cursor.fetchall()]
    conn.close()
    return users
@app.route('/')
def index():
    users = get_users()
    return render_template("index.html", users = users)
@app.route('/chat/<username>')
def chat(username):
    return render_template('chat.html', username=username)

@socketio.on('join')
def on_join(data):
    """User joins a chat room"""
    room = data['room']
    join_room(room)
    emit('message', {"message": f"{data['username']} has joined the chat"}, room=room)

@socketio.on('message')
def handle_message(data):
    """Handle incoming messages"""
    username = data['username']
    message = data['message']
    room = data['room']

    # Save message to a text file
    chat_file = f"messages/{room}.txt"
    with open(chat_file, "a") as f:
        f.write(f"{username}: {message}\n")

    emit('message', {"username": username, "message": message}, room=room)

@socketio.on('leave')
def on_leave(data):
    """User leaves a chat room"""
    room = data['room']
    leave_room(room)
    emit('message', {"message": f"{data['username']} has left the chat"}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)