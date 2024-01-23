import paho.mqtt.client as mqtt

from pypglab.mqtt import Client, Sub_State, Subcribe_CallBack

MQTT_SERVER = "localhost"
MQTT_PORT = 1883
MQTT_USERNAME = "pierluigi"
MQTT_PASSWORD = "password"

PGLAB_DISCOVERY_TOPIC = "pglab/discovery"


class MQTT:
    """MQTT Client class to comunicate with PG LAB device using paho MQTT library."""
    
    def __init__(self) -> None:
        """Initiliaze."""

        def on_connect(client, userdata, flags, rc):
            """The callback for when the client receives a CONNACK response from the server."""
            self._connected = True


        def on_disconnect(client, userdata, rc):
            self._connected = False
        
        def on_message(client, userdata, msg):
            """Callback when a message has been received on a topic that the client subscribes."""

            if msg.topic.startswith(PGLAB_DISCOVERY_TOPIC):
                self._discovery.append( (msg.topic, msg.payload) )
                return 
            
            if userdata is None:
                # this should never happen
                return

            # do the callback
            callback = userdata.get(msg.topic)
            if callback:
                payload = msg.payload.decode("utf-8")
                callback(msg.topic, payload)


        self._connected = False
        self._discovery = []
        self._subscribe_callback:dict = {}
        self._mqtt_client = mqtt.Client()
        self._mqtt_client.on_connect = on_connect
        self._mqtt_client.on_disconnect = on_disconnect
        self._mqtt_client.on_message = on_message
        self._mqtt_client.user_data_set(self._subscribe_callback)
        self._mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        # create a mqtt client for pglab used for pglab python module
        self._pglab_mqtt_client : Client = None

    def setup(self)->None:

        async def mqtt_publish(
            topic: str, payload: str, qos: int | None = 0, retain: bool | None = False
        ) -> None:
            self._mqtt_client.publish(topic, payload, qos, retain)

        async def mqtt_subscribe(
            sub_state: Sub_State, topic: str, callback_func: Subcribe_CallBack
        ) -> Sub_State:
            
            self._subscribe_callback[topic] = callback_func
            self._mqtt_client.subscribe(topic, qos=0)

            new_substate = {}
            new_substate[topic] = callback_func

            self._subscribe_callback[topic] = callback_func

            return new_substate

        async def mqtt_unsubscribe(sub_state: Sub_State) -> None:
            for topic in sub_state:
                self._mqtt_client.unsubscribe(topic)

        # connect with MQTT broker
        self._mqtt_client.connect(MQTT_SERVER, MQTT_PORT, 60)

        # setup the MQTT PGLAB client interface
        self._pglab_mqtt_client = Client(mqtt_publish, mqtt_subscribe, mqtt_unsubscribe)

        # setup to PGLAB discovery message
        self._mqtt_client.subscribe(PGLAB_DISCOVERY_TOPIC + "/#")

    def start(self) -> None:
        """Start the MQTT Loop."""
        self._mqtt_client.loop_start()

    def stop(self) -> None:
        """Stop the MQTT Loop."""
        self._mqtt_client.loop_stop()

    @property
    def discovery(self) :
        return self._discovery
    
    @property
    def pglab_mqtt_client(self):
        return self._pglab_mqtt_client
    
    @property
    def connected(self):
        return self._connected


