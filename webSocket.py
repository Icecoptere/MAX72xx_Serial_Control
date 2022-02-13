from flask import Flask, request, send_file, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import threading
import matrixController as mat

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, static_url_path="/static")
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


def runTheServer():
    socketio.run(app, host='0.0.0.0', port=9009)


@socketio.on('connectionACK')
def connectionACK(json):
    print('received json: ' + str(json))
    socketio.emit("updateFromBack", {'data': "Back responded"})


@socketio.on('updateFront')
def updateFront(json):
    if json['type'] == "cycle":
        theCycle = json['data']
        if theCycle == 0:
            mat.doStandardCycle()
        elif theCycle == 1:
            mat.doOtherCycle()
    elif json['type'] == "newMatrix":
        newMatrix = json['data']
        mat.sendMatrix(newMatrix)


@app.route("/")
def defaultPage():
    return send_from_directory('', "static/index.html")


@app.route("/static/<filename>")
def returnStatic(filename):
    return send_from_directory('static', filename)


def createUpdate(json):
    socketio.emit("updateFromBack", {'data': json})


mat.initConnection()
threading.Thread(target=runTheServer).start()
