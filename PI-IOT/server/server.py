from collections import defaultdict
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

from paho.mqtt import publish

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
# executor = Executor(app)
# InfluxDB Configuration
token = "_HTXQFGOBP4arFCaIQTdP6jGHSVMhPSzfvDfsf36i9bDX9-Z5hNphr7Q2APw_rLoOy6WeVVWOIYH-ZTDb6xUEA=="
org = "ftn"
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
    client.subscribe("ALARM ACTIVATION")
    client.subscribe("ALARM DEACTIVATION")
    client.subscribe("Bedroom RGB")


def process_and_emit(data):
    emit('update_data', data, namespace='/')


latest_mqtt_message = None


@app.route('/get-latest-mqtt-message')
def get_latest_mqtt_message():
    global latest_mqtt_message
    return jsonify(latest_mqtt_message)


def combined_on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode('utf-8'))
        if message.topic == "frontend/update":
            socket_bucket["front_data"].append(data)
            print(data)
        elif message.topic in ["ALARM ACTIVATION", "ALARM DEACTIVATION"]:
            data = json.loads(message.payload.decode('utf-8'))
            event_type = "Activation" if message.topic == "ALARM ACTIVATION" else "Deactivation"
            print(data["Sensor"] + " " + event_type)
            save_alarm_to_db(event_type, data["Sensor"])
        else:
            save_to_db(data)
    except Exception as e:
        print(f"Error handling message: {e}")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = combined_on_message


def save_alarm_to_db(event_type, sensor):
    now = datetime.utcnow().isoformat()
    value = 1 if event_type == "Activation" else 0
    alarm_event_payload = {
        "measurement": "Alarm Event",
        "tags": {
            "event_type": event_type,
            "trigggered_by": sensor,
        },
        "time": now,
        "fields": {
            "value": value
        }
    }
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = Point.from_dict(alarm_event_payload)
    write_api.write(bucket=bucket, org=org, record=point)


# mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))
# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')
#     socketio.start_background_task(target=test_emit2)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    test_emit2()


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('get_data')
def messaging(message, methods=['GET', 'POST']):
    print('received message: ' + str(message))
    for key in socket_bucket:
        for value in socket_bucket[key]:
            socketio.emit(key, value, room=request.sid)
        socket_bucket[key] = []


def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    if "id" not in data:
        data["id"] = 1
    timestamp = datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow()
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("value", data["value"])
        .time(timestamp)
    )
    write_api.write(bucket=bucket, org=org, record=point)


# Route to store dummy data
@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        store_data(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/button_pressed', methods=['POST'])  # Promenite u POST
def get_color_from_front():
    data = request.json
    button_pressed = data['button_pressed']
    print(button_pressed + " OVO SAM DOBILA HEHEH")
    topic = "server/button_pressed"
    payload = json.dumps({"button_pressed": button_pressed})
    publish.single(topic, payload=payload, hostname="localhost", port=1883)
    return jsonify({"message": "Received button_pressed: " + button_pressed})


@app.route('/proba', methods=['GET'])
def proba():
    socketio.emit('data_testing', {"message": "wtf"})
    return jsonify({"message": "wtf"})


def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def test_emit2():
    test_data = {'message': 'Hello from Flask!'}
    socketio.emit('test_message', test_data)
    return jsonify({"status": "success", "message": "Test data emitted"})


@app.route('/test_emit')
def test_emit():
    test_data = {'message': 'Hello from Flask!'}
    print(test_data)
    return jsonify({"status": "success", "message": "Test data emitted"})


@app.route('/simple_query', methods=['GET'])
def retrieve_simple_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Temperature")"""
    return handle_influx_query(query)


@app.route('/aggregate_query', methods=['GET'])
def retrieve_aggregate_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Humidity")
    |> mean()"""
    return handle_influx_query(query)


if __name__ == '__main__':
    # socketio.init_app(app)
    socketio.run(app, debug=True, use_reloader=False)
