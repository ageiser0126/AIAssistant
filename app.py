from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit, join_room, close_room
import ai_client
import hubspot_client
import sql_client

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
rooms = []
sql_client.setup_database()

# configure the socketio logging
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def index():
    return render_template('base.html')

@socketio.on("connect")
def handle_connect(params):
    print("Client connected: " + request.sid)
    existingThread = params["threadId"]

    if existingThread == "NONE":
        thread = ai_client.create_new_thread()

        join_room(thread.id)
        rooms.append({"sid": request.sid, "thread": thread.id})

        messages = ai_client.start_session_stream(thread)
        for m in messages:
            if m.role == "assistant":
                emit("new_message", {"output": m.content[0].text.value, "query": "NONE", "threadId": thread.id},
                     to=thread.id, broadcast=True)

    else:
        thread = ai_client.client.beta.threads.retrieve(existingThread)

        join_room(thread.id)
        rooms.append({"sid": request.sid, "thread": thread.id})

        messages = ai_client.get_response(thread.id)
        for m in messages:
                emit("load_messages", {"output": m.content[0].text.value, "role": m.role, "query": "NONE", "threadId": thread.id},
                     to=thread.id, broadcast=True)

@socketio.on("message")
def handleMessage(data):
    print("Input From: " + request.sid)
    emit("new_message", {"output": data["input"], "role": "user", "query": data["input"],
                         "threadId": data["threadId"]}, to=data["threadId"], broadcast=True)


    messages = ai_client.post_message_stream(data["threadId"], data["input"])
    last_item = None
    for item in messages:
        last_item = item

    if last_item.role == "assistant":
        emit("new_message", {"output": last_item.content[0].text.value, "role": last_item.role, "query": data["input"],
                             "threadId": data["threadId"]}, to=data["threadId"], broadcast=True)


@socketio.on("disconnect")
def handle_disconnect():
    for room in rooms:
        if room["sid"] == request.sid:
            close_room(room["thread"])
            rooms.remove(room)
            messages = ai_client.get_response(room["thread"])

            list_of_messages = []

            #write to array
            for m in messages:
                if m.role == "user" and m.content[0].text.value != "NONE" and m.content[0].text.value != "":
                    list_of_messages.append("User: " + m.content[0].text.value + "\n")
                if m.role == "assistant":
                    list_of_messages.append("Assistant: " + m.content[0].text.value + "\n")

            if len(list_of_messages) > 4:

                #send to Hubspot
                hubspot_client.create_ticket(list_of_messages)

                #save to database
                sql_client.add_full_history(room["thread"], list_of_messages)

                for m in messages:
                    if m.role == "user" and m.content[0].text.value != "NONE" and m.content[0].text.value != "":
                        sql_client.add_history(room["thread"], m.role, m.content[0].text.value)
                    if m.role == "assistant":
                        sql_client.add_history(room["thread"], m.role, m.content[0].text.value)


    print("Client disconnected: " + request.sid)


if __name__ == "__main__":
    socketio.run(app, debug=True, host='127.0.0.1', port=8000)
