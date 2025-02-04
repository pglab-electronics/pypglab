import asyncio
import time

from pypglab.helper import pyPgLab

MQTT_SERVER = "192.168.1.8"
MQTT_PORT = 1883
MQTT_USERNAME = "pierluigi"
MQTT_PASSWORD = "password"

E_BOARD_NAME = "E-BOARD-DD53AC85"

def turn_relay(relay, on):
    if on:
        asyncio.run( relay.turn_on() )
    else:
        asyncio.run( relay.turn_off() )
    time.sleep(0.02)

pglab = pyPgLab()
pglab.start(MQTT_SERVER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD)
pglab.connect()

e_board = pglab.get_device_by_name(E_BOARD_NAME)

if e_board:
    # turn all relay outputs ON
    for relay in e_board.relays:
        turn_relay(relay, True)

    #turn all relay outputs OFF
    for relay in reversed(e_board.relays):
        turn_relay(relay, False)

pglab.stop()

