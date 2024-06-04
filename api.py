from flask import Flask, jsonify
from threading import Thread
import processing

app = Flask(__name__)

#@app.route('[command]', methods=['GET / POST / DELETE / UPDATE'])
#ex: @app.route('/date', methods=['GET'])

@app.route('/date', methods=['GET'])
def get_convo():
    result = processing.conversation
    return jsonify({'conversation': result})

@app.route('/message', methods=['GET'])
def get_cal():
    result = processing.Decoded_Message
    return jsonify({'Decoded_Message': result})

if __name__ == '__main__':
    print("Thread starting")
    thread = Thread(target = processing.app, name="Processing")
    thread.start()
    app.run()