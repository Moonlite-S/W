from flask import Flask
from threading import Thread
import processing

app = Flask(__name__)

#@app.route('[command]', methods=['GET / POST / DELETE / UPDATE'])
#ex: @app.route('/date', methods=['GET'])

@app.route('/convo')
def get_convo():
    result = processing.conversation
    return {'conversation': result}

if __name__ == '__main__':
    print("Thread starting")
    thread = Thread(target = processing.app, name="Processing")
    thread.start()
    app.run()