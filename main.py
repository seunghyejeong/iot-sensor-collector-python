from paho.mqtt import client as mqtt
from flask import Flask, request, jsonify, Response
import time

class AccelerationData:
    def __init__(self, x, y, z):
        self.x =  float(x)
        self.y = float(y)
        self.z = float(z)

class LocationData:
    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

app = Flask(__name__)

host = "localhost"
port = 1883
topic = "test/topic"
client_id = "python_mqtt_client"

def connect_mqtt() -> mqtt.Client:

    client = mqtt.Client(client_id=client_id, clean_session=True, userdata=None, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.subscribe(topic=topic)
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected with result code", rc)
        else:
            print("Failed to connect return code", rc)

    def on_disconnect(client, userdata, flags, rc=0):
        print(f"disconnected result code {str(rc)}")

    def on_log(client, userdata, level, buf):
        print(f"log: {buf}")
    
    # 메시지 수신 콜백 함수
    def on_message(client, userdata, message):
        print(f"Received message: {message.payload.decode()} on topic {message.topic}")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log
    client.on_message = on_message  # 메시지 수신 콜백 설정

    client.connect(host=host, port=port)
    client.loop_start()  # 비동기 MQTT 루프 시작
    return client

@app.route('/acceleration', methods=['POST'])
def postAcceleration():
    data = request.json

    print("Received data:", data)

    if data is None:
        return jsonify("No data"), 400
    try:
        acceleration_data = AccelerationData(data['x'], data['y'], data['z'])
    except KeyError:
        return jsonify({"error": "Acceleration Data missing in JSON data"}), 400

    return jsonify({"message": "Acceleration Data received",
                    "x": acceleration_data.x,
                    "y": acceleration_data.y,
                    "z": acceleration_data.z}), 200

@app.route('/location', methods=['POST'])
def postLocation():
    data = request.json

    if data is None:
        return jsonify("No data"), 400
    try:
        location_data = LocationData(data['latitude'], data['longitude'])
    except KeyError:
        return jsonify({"error": "Location data missing in JSON data"}), 400

    return jsonify({"message": "Location Data received",
                    "latitude": location_data.latitude,
                    "longitude": location_data.longitude}), 200

if __name__ == '__main__':
    connect_mqtt()
    app.run(host='0.0.0.0', debug=True, port=8080)
