"""Helper to find pglab device"""

import asyncio
import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json

from .const import PGLAB_DISCOVERY_TOPIC
from .device import Device
from .mqtt import Client, Subscribe_CallBack, Sub_State

class pyPgLab():
    def __init__(self):
        self._devices = []
        self._subscribe_topic_callback = {}
        self._mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self._mqtt_client.on_message = pyPgLab.on_mqtt_message
        self._mqtt_client.on_connect = pyPgLab.on_mqtt_connect        
        self._mqtt_client.user_data_set(self)
        self._mqtt_server_host = ''
        self._mqtt_server_port = 0
        self._mqtt_server_username = ''
        self._mqtt_server_password = ''

    def on_mqtt_connect(client, userdata, flags, reason_code, properties):
        """ callback from mqtt client when connection is been established """

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(PGLAB_DISCOVERY_TOPIC + "/#")

    def on_mqtt_message(client, userdata, msg):
        """ callback from mqtt client when a new message is been received """   

        async def publish( topic: str, payload: str, qos: int | None = 0, retain: bool | None = False) -> None:
            client.publish(topic, payload, qos, retain)

        async def subscribe(sub_state: Sub_State, topic: str, callback_func: Subscribe_CallBack) -> Sub_State:
            userdata._subscribe_topic_callback[topic] = callback_func
            client.subscribe(topic)
            sub_state = { "topic": topic, "callback": callback_func}
            return sub_state

        async def unsubscribe(sub_state: Sub_State):
            topic = sub_state["topic"]            
            client.unsubscribe(topic)
            del userdata._subscribe_topic_callback[topic]

        # check if there is a callback to call for the received message
        if msg.topic in userdata._subscribe_topic_callback:
            callback  =  userdata._subscribe_topic_callback[msg.topic]
            callback(msg.topic, msg.payload.decode("utf-8"))
            return None                

        # check if the message is a discovery of a new PG LAB device
        if msg.topic.startswith(PGLAB_DISCOVERY_TOPIC):
            discovery_msg = json.loads(msg.payload)

            # create the PG LAB Electronics device
            device = Device()
            asyncio.run( device.config(Client(publish, subscribe, unsubscribe), discovery_msg, True) )
            userdata._devices.append(device)

    def start(self, host, port = 1883, username = '', password = ''):
        """ start the client loop with mqtt broker """
        self._mqtt_server_host = host
        self._mqtt_server_port = port
        self._mqtt_server_username = username
        self._mqtt_server_password = password        
        self._mqtt_client.loop_start()

    def connect(self):
        """ connect to the mqtt broker """        
        self._mqtt_client.username_pw_set(self._mqtt_server_username, self._mqtt_server_password)
        self._mqtt_client.connect(self._mqtt_server_host, self._mqtt_server_port, 60)

    def stop(self):
        """ stop the client loop with mqtt broker """
        self._mqtt_client.loop_stop()

    def get_device_by_name(self, name, timeout = 2):
        """ get a pg lab device by the name """
        start = time.time()

        while 1:
            for device in self._devices:
                if device.name == name:
                    return device

            if (time.time() - start) > timeout:
                 return None
            
            # wait a bit before to check again if the device is been discovered
            time.sleep(0.1)

        return None

    @property
    def devices(self):
        """Get the device array."""
        return self._devices