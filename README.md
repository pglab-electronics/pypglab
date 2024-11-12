
# pypglab

## About

An asynchronous Python library to communicate with PG LAB Electronics devices over MQTT.

This library was created for Home Assistant integrations of PG LAB Electronics.

## Features

- Discover devices
- Controll relays (turn on/off)
- Monitor relays status (on/off)
- Controll shutters (open/close/pause)
- Monitor shutters status (open/opening/closed/closing)
- Receiving device internal sensor update

## Devices supported
- E-Board 

## Comming soon
- E-Switch

## Installation

```sh
pip install pypglab
```

## Usage

A client interface in pypglab/mqtt.py is used for the communication with MQTT broker.
The interface exposes callback for: publish, subscribe and unsubscribe.
Who is using pypglab library must manage the MQTT connection and define the MQTT client callback.

The following is a pseudo example that turn on all relays.

```python
from pypglab.device import Device
from pypglab.mqtt import Client

async def setup_pglab_device(config:dict):
  async def mqtt_publish( topic: str, payload: str, qos: int | None = 0, retain: bool | None = False) -> None:
      print("TODO... call the client MQTT publish")

  pglab_mqtt_client = Client(mqtt_publish, None, None)
  pglab_device = Device()
  await pglab_device.config(pglab_mqtt_client, config, True)

  for relay in pglab_device.relays:
      await relay.turn_on() 

```

For working example and proper setup of the MQTT connection and callback, 
see the example.py and the unittest of pypglab python library.

## Feedback

Please give us feedback on pglab.electronics@gmail.com

## Founder

This plugin is created by PG Lab Electronics.

## License

Code is released under [MIT license]
