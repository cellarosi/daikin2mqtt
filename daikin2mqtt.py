import os

from paho.mqtt.client import Client
from prometheus_client import start_http_server, Gauge
from daikinapi import Daikin

g = Gauge('clima_sensor_value', 'Temperatura dal climatizzatore sala', ['name'])
API = Daikin("192.168.1.61")

client = Client(client_id = "collector")
client.username_pw_set(username=os.getenv('MQTT_USERNAME'),password=os.getenv('MQTT_PASSWORD'))
client.connect(os.getenv('MQTT_HOST'))

def process_request():
    inside = API.inside_temperature
    outside = API.outside_temperature
    g.labels(name='temperatura_esterna').set(outside)
    g.labels(name='temperatura_interna').set(inside)

    client.publish(topic = "soggiorno/temperatura", payload = inside) 
    client.publish(topic = "esterno/temperatura", payload = outside) 

   
if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request()
