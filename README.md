
# pypglab

## About

An asynchronous Python library to communicate with PG LAB Electronics devices over MQTT.

This library was created for Home Assistant integrations of PG LAB Electronics.

## Features

- Discover devices
- Control relays (turn on/off)
- Monitor relays status (on/off)
- Control shutters (open/close/pause)
- Monitor shutters status (open/opening/closed/closing)
- Receiving device internal sensor update

## Devices supported
- E-BOARD

## Coming soon
- E-SWITCH

## Installation

```sh
pip install pypglab
```

## Usage

The library has an helper class to simplify the discovery and the use of PG LAB Electronics devices.
The helper class hide the complexity to setup the MQTT connection with the broker.

In this simple working example pyPgLab class does the connection with the MQTT broker, retrieve an E-BOARD 
device and turn ON all available relay outputs

```python

from pypglab.helper import pyPgLab

def turn_relay(relay, on):
    if on:
        asyncio.run( relay.turn_on() )
    else:
        asyncio.run( relay.turn_off() )
    time.sleep(0.02)

pglab = pyPgLab()
pglab.start("192.168.1.8")
pglab.connect()

e_board = pglab.get_device_by_name("E-BOARD-DD53AC85")

if e_board :
    # turn all relay outputs ON
    for relay in e_board.relays:
        asyncio.run( relay.turn_on() )

pglab.stop()

```

For more example and proper setup of the MQTT connection and callback, 
see the example.py and the unittest of pypglab python library.

## Feedback

Please give us feedback on support@pglab.dev

## Founder

This plugin is created by PG Lab Electronics.

## License

Code is released under [MIT license]
