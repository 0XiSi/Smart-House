import json
import paho.mqtt.client as paho
import threading
from asgiref.sync import async_to_sync
from home.models import Relay, DH11
from channels.layers import get_channel_layer
from .consumers import RelayStateConsumer, SensorConsumer
from queue import Queue

# Queue to communicate between MQTT thread and Django views
mqtt_message_queue = Queue()

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    client.subscribe("esp8266_data")
    client.subscribe("esp8266_DH11_data")

def on_message(client, userdata, msg):
    print("Received a message from topic: " + msg.topic)
    print("Message payload: " + str(msg.payload))

    if msg.topic == "esp8266_data":
        # Extract the MAC address and state from the message payload
        data = json.loads(msg.payload)
        mac_addr = data.get('mac_addr')
        state = data.get('state')

        # Update the relay state in the database
        try:
            relay = Relay.objects.get(mac_addr=mac_addr)
            relay.state = state
            relay.save()
            print(f"Relay state updated: MAC address={mac_addr}, State={state}")

            # Notify clients of the state change via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "relay_updates",
                {"type": "relay_state_update", "mac_addr": mac_addr, "state": state}
            )
        except Relay.DoesNotExist:
            print(f"No relay found with MAC address: {mac_addr}")
    elif msg.topic == "esp8266_DH11_data":
        data = json.loads(msg.payload)
        mac_addr = data.get('mac_addr')
        temp = data.get('temperature')
        humidity = data.get('humidity')

        # Update the sensor state in the database
        try:
            sensor = DH11.objects.get(mac_addr=mac_addr)
            sensor.temp = temp
            sensor.humidity = humidity
            sensor.save()
            print(f"Sensor state updated: MAC address={mac_addr}, Temp={temp}, Humidity={humidity}")

            # Notify clients of the state change via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "sensor_updates",
                {"type": "sensor_update", "mac_addr": mac_addr, "temperature": temp, "humidity": humidity}
            )
        except DH11.DoesNotExist:
            print(f"No sensor found with MAC address: {mac_addr}")

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5, callback_api_version=paho.CallbackAPIVersion.VERSION2)
client.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)

def mqtt_client_thread():
    client.on_connect = on_connect
    client.on_message = on_message
    # client.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)
    client.username_pw_set("hivemq.webclient.1710770407588", "%C,H0BWgnF5he<2vd6M.")
    client.connect("85a4979f4e39416e9fabd326a49b02a6.s1.eu.hivemq.cloud", 8883)
    client.loop_forever()

# Start MQTT client thread
mqtt_thread = threading.Thread(target=mqtt_client_thread)
mqtt_thread.daemon = True
mqtt_thread.start()
