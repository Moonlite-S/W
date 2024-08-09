import json
from threading import Thread
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import processing

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
thread = None

#@app.route('[command]', methods=['GET / POST / DELETE / UPDATE'])
#ex: @app.route('/date', methods=['GET'])

@app.route('/api/convo', methods=['GET'])
def get_convo():
    convo = processing.conversation
    my_input = ""
    w_latest_message = ""

    for i in reversed(convo):
        if i['role'] == 'user':
            my_input = i['content']
            break

    for i in reversed(convo):
        if i['role'] == 'assistant':
            w_latest_message = i['content']
            break

    data = {"W": w_latest_message, "Muna": my_input}
    return json.dumps(data)

@socketio.on('connect')
def connected(data):
    print("client has connected")
        
@socketio.on("disconnect")
def disconnected(d):
    global thread
    print("user disconnected")

    if thread is not None:
        print("stopping background thread")
        thread.join(10.0)
        print(thread.is_alive())
        #thread = None

@socketio.on('server_loop')
def main_loop():
    global thread
    if thread is None:
        print("starting background thread")
        thread = socketio.start_background_task(processing.main_loop())
        thread.start()

def main():
    processing.init_processing()
    print("Server starting")
    socketio.run(app, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main()
