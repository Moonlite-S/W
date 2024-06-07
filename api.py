from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread
import processing

app = Flask(__name__)
cors = CORS(app, origins='*')

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

    return jsonify({'W': w_latest_message, 'Muna': my_input})

@app.route('/api/pause', methods=['POST'])
def post_paused_convo():
    processing.paused = True
    return jsonify({'Paused': 'True'})

@app.route('/api/resume', methods=['POST'])
def post_resumed_convo():
    processing.paused = False
    return jsonify({'Paused': 'False'})

if __name__ == '__main__':
    print("Thread starting")
    thread = Thread(target = processing.app, name="Processing")
    thread.start()
    app.run(port=5000)