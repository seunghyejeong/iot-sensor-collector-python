# 필요한 패키지 import
from paho.mqtt import client as mqtt
from flask import Flask, request, jsonify

# 변수 선언
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

# # 기능 구현
# # 1. mqtt 
# Broker와 연결 테스트 
host = "localhost"
port = 1883
topic = "test/topic"
client_id = "python_mqtt_client"

def connect_mqtt() -> mqtt.Client :
    def on_connect(client, userdata, flags, rc, properties=None):  
        if rc == 0:
            print("Connected with result code", rc)  
            client.subscribe(topic)
        else:
            print("Failed to connect return code", rc)  
    def on_disconnect(client, userdata, flags, rc=0):
        print(f"disconnected result code {str(rc)}")

    def on_log(client, userdata, level, buf):
        print(f"log: {buf}")
                    
    client = mqtt.Client(client_id=client_id, clean_session=True, userdata=None, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log=on_log
    client.connect(host=host, port=port)
    client.loop
    return client


# # 2. post acceleration
@app.route('/acceleration', methods=['POST'])
def postAcceleration():
    data = request.json

    if data is None :
        return jsonify("No data"), 400
    try:
        acceleration_data = AccelerationData(data['x'],data['y'],data['z'])
    except KeyError:
        return jsonify({"error": "Acceleration Data missing in JSON data"}), 400
    
    return jsonify({"message": "Acceleration Data received", 
                    "x": acceleration_data.x, 
                    "y": acceleration_data.y,
                    "Z": acceleration_data.z}), 200

# # 3. post location
@app.route('/location', methods=['POST'])
def postLocation():
    data = request.json
    
    if data is None: 
        return jsonify("No data"), 400
    try:
        location_data = LocationData(data['latitude'], data['longitude'])
    except KeyError:
        return jsonify({"error" : "Location data missing in JSON data"}), 400
    
    return jsonify({"message" : "Location Data received",
                    "latitude" : location_data.latitude,
                    "longitude" : location_data.longitude}), 200
def run():
    client = connect_mqtt()
    client = connect_mqtt()  # MQTT 클라이언트 연결
    client.loop_start()
    print(f"connect to broker {host}:{port}")

if __name__ == '__main__':
    run()