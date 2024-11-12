import asyncio
import time
import paho.mqtt.client as mqtt

from pypglab.device import Device
from pypglab.mqtt import Client

MQTT_SERVER = "localhost"
MQTT_PORT = 1883
MQTT_USERNAME = "pierluigi"
MQTT_PASSWORD = "password"


async def mqtt_publish( topic: str, payload: str, qos: int | None = 0, retain: bool | None = False) -> None:
    mqtt_client.publish(topic, payload, qos, retain)


mqtt_client = mqtt.Client()
mqtt_client.loop_start()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, 60)

# wait the connection with the broker
time.sleep(1)

pglab_mqtt_client = Client(mqtt_publish, None, None)

config = {
    "ip":"192.168.1.16", 
    "mac":"80:34:28:1B:18:5A", 
    "name":"e-board-office", 
    "hw":"255.255.255", 
    "fw":"255.255.255", 
    "type":"E-Board", 
    "id":"E-Board-DD53AC85", 
    
    "manufacturer":"PG LAB Electronics", 
    "params":{
        "shutters":3, 
        "boards":"10000000" 
    }
}

pglab_device = Device()
asyncio.run( pglab_device.config(pglab_mqtt_client, config, True) )

for relay in pglab_device.relays:
    asyncio.run( relay.turn_on() )

mqtt_client.loop_stop()
