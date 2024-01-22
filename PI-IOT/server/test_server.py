import time
from flask import Flask, jsonify, request, copy_current_request_context, current_app
from flask_socketio import SocketIO
from flask_socketio import emit
from flask_cors import CORS
# from flask_executor import Executor
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import paho.mqtt.client as mqtt
import json
from collections import defaultdict 


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

token = "oSuV0hFfljDaUenNeV7NBRPsHMFjMwYyyGBGTkm-ePU2D46TXTFdbfHOkzk1i7y88ZXGdVG5Ev6AAD_Af1SzbA=="
org = "FTN"
url = "http://localhost:8086"
bucket = "bucket_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)
# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()
socket_bucket = defaultdict(lambda: [])


def on_connect(client, userdata, flags, rc):
    client.subscribe("Key")
    client.subscribe("Temperature")
    client.subscribe("Humidity")
    client.subscribe("Motion")
    client.subscribe("DoorBuzzer")
    client.subscribe("Door Status")
    client.subscribe("Door Ultrasonic Sensor")
    client.subscribe("Door Motion Sensor")
    client.subscribe("Door Light")
    client.subscribe("Bedroom Infrared")
    client.subscribe("frontend/update")


def combined_on_message(client, userdata, message):
        try:
            data = json.loads(message.payload.decode('utf-8'))
            if message.topic == "frontend/update":
                socket_bucket["front_data"].append(data)
        except:
             print("something went wrong")
    #     pass
    # else:
    #     # save_to_db(data)
    #     pass

# def emit_updated_data(data):
#     socketio.emit('message', {'data': data})

# def save_to_db(data):
#     write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
#     if "id" not in data:
#         data["id"] = 1
#     timestamp = datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow()
#     point = (
#         Point(data["measurement"])
#         .tag("simulated", data["simulated"])
#         .tag("runs_on", data["runs_on"])
#         .tag("name", data["name"])
#         .field("value", data["value"])
#         .time(timestamp)
#     )
#     write_api.write(bucket=bucket, org=org, record=point)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = combined_on_message


users = {}
@socketio.on('disconnect')
def on_disconnect():
    users.pop(request.sid,'No user found')
    socketio.emit('current_users', users)
    print("User disconnected!\nThe users are: ", users)

@socketio.on('sign_in')
def user_sign_in(user_name, methods=['GET', 'POST']):
    users[request.sid] = user_name['name']
    socketio.emit('current_users', users)
    print("New user sign in!\nThe users are: ", users)

@socketio.on('test_message')
def messaging(message, methods=['GET', 'POST']):
    print('received message: ' + str(message))
    message['from'] = request.sid
    for key in socket_bucket:  
        for value in socket_bucket[key]:
            socketio.emit(key, value, room=request.sid)
    del(socket_bucket[key])


if __name__ == '__main__':
    socketio.run(app, debug=True)