from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
from datetime import datetime
import json

app = Flask(__name__)

# InfluxDB Configuration
token = "qdZgg86WG5M2xFMVqx4Wu0z_yskrv5Wukt-dGA_ze6nyRSvjs9FXBjQV2rIhCtF2fYcc_bzmGphraOSKR7_fTQ=="  # izgenerise se na sajtu
org = "FTN"
url = "http://localhost:8086"
bucket = "smarthomeiot4"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)



# MQTT Configuration

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


def on_connect(client, userdata, flags, rc):
    client.subscribe("Door Status")
    client.subscribe("Door Ultrasonic Sensor")
    client.subscribe("Door Motion Sensor")



mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))


def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    timestamp = datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow()
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(timestamp)
    )
    write_api.write(bucket=bucket, org=org, record=point)


if __name__ == '__main__':
    app.run(debug=True)
