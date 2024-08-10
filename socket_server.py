from flask import Flask, copy_current_request_context
from flask_cors import CORS
from flask_socketio import SocketIO
import backend

# TODO:
# - Add Error Handling
# - Fix Server / Thread Issues

# Global Vars for the Server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
thread_stop = False # Used to stop the thread
thread = None

@socketio.on('connect')
def connected():
    print("Client has connected")
        
@socketio.on("disconnect")
def disconnected():
    global thread, thread_stop
    print("user disconnected")

    if thread is not None:
        print("Stopping Backend Thread")
        thread_stop = True
        thread.join()
        
        print(thread.is_alive())
        thread = None

@socketio.on('server_loop')
def server_loop():
    global thread, thread_stop

    # This ensures that the required socket context is applied
    @copy_current_request_context
    def backend_loop():
        while not thread_stop:
            backend.main_loop()

    if thread is None:
        print("Starting Backend Thread")
        thread = socketio.start_background_task(backend_loop)

def main():

    ''' Main Function to run the whole application.. '''
    backend.init_processing()
    print("Server starting")
    socketio.run(app, host='127.0.0.1', port=5000)