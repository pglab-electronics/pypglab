"""Constants used by pypglab."""

import logging
from typing import Final

LOGGER = logging.getLogger(__name__)

PGLAB_VERSION = "0.0.1"

# All devices managed by this python library
E_BOARD: Final = "E-BOARD"
E_RELAY: Final = "E-RELAY"
E_SWITCH: Final = "E-SWITCH"

MANUFACTURER: Final = "PG LAB Electronics"

# The following define the device type name
PGLAB_DEVICE_TYPES = {
    E_BOARD: "E-Board",
    E_RELAY: "E-Relay",
    E_SWITCH: "E-Switch",
}

TOPIC_PGLAB: Final = "pglab"

# Discovery message fields
CONFIG_MAC: Final = "mac"
CONFIG_IP: Final = "ip"
CONFIG_ID: Final = "id"
CONFIG_NAME: Final = "name"
CONFIG_TYPE: Final = "type"
CONFIG_MANUFACTOR: Final = "manufacturer"
CONFIG_HARDWARE_VERSION: Final = "hw"
CONFIG_FIRMWARE_VERSION: Final = "fw"
CONFIG_PARAMETERS: Final = "params"
CONFIG_EBOARD_SHUTTERS: Final = "shutters"
CONFIG_EBOARD_BOARDS: Final = "boards"

# Available entities
ENTITY_RELAY: Final = "relay"
ENTITY_SHUTTER: Final = "shutter"
ENTITY_SWITCH: Final = "switch"
ENTITY_SENSOR: Final = "sensor"

# Relay
RELAY_STATE_ON: Final = "ON"
RELAY_STATE_OFF: Final = "OFF"

# Shutter MQTT state
SHUTTER_STATE_OPENING: Final = "OPENING"
SHUTTER_STATE_OPEN: Final = "OPEN"
SHUTTER_STATE_CLOSING: Final = "CLOSING"
SHUTTER_STATE_CLOSED: Final = "CLOSED"

# Shutter MQTT command
SHUTTER_CMD_OPEN: Final = "OPEN"
SHUTTER_CMD_CLOSE: Final = "CLOSE"
SHUTTER_CMD_STOP: Final = "STOP"

# MQTT topic for set and get state
ENTITY_TOPIC = {
    ENTITY_RELAY: ("set", "state"),
    ENTITY_SHUTTER: ("set", "state"),
    ENTITY_SENSOR: (None, "value"),
}

# Sensors value
SENSOR_TEMPERATURE: Final = "temp"
SENSOR_VOLTAGE: Final = "volt"
SENSOR_REBOOT_TIME: Final = "rtime"

# Sensors configuration for a specific PG LAB device
SENSOR_CONFIG = {
    "E-Board": [SENSOR_TEMPERATURE, SENSOR_VOLTAGE, SENSOR_REBOOT_TIME],
    "E-Relay": [],
    "E-Switch": [],
}
