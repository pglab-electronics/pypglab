""" A device for pypglab."""

from __future__ import annotations

from typing import cast
from voluptuous import Schema, ALLOW_EXTRA, REMOVE_EXTRA, MultipleInvalid

from . import validation as cv

from .const import (
    E_BOARD, 
    E_SWITCH, 
    LOGGER, 
    PGLAB_DEVICE_TYPES, 
    SENSOR_CONFIG, 
    CONFIG_MAC, 
    CONFIG_IP, 
    CONFIG_ID, 
    CONFIG_NAME, 
    CONFIG_PARAMETERS,
    CONFIG_TYPE, 
    CONFIG_MANUFACTOR, 
    CONFIG_HARDWARE_VERSION, 
    CONFIG_FIRMWARE_VERSION,
    CONFIG_EBOARD_SHUTTERS,
    CONFIG_EBOARD_BOARDS,
)

from .mqtt import Client
from .relay import CreateRelay
from .sensor import CreateSensor
from .shutter import CreateShutter


PGLAB_DISCOVERY_SCHEMA = Schema(
    {
        CONFIG_MAC: cv.macaddrs,
        CONFIG_IP: cv.ipaddrs,
        CONFIG_ID: cv.string,
        CONFIG_NAME: cv.string,
        CONFIG_TYPE: cv.devicetype,
        CONFIG_MANUFACTOR: cv.manufacturer,
        CONFIG_HARDWARE_VERSION: cv.version,
        CONFIG_FIRMWARE_VERSION: cv.version,
    },
    required=True,
    extra=ALLOW_EXTRA,
)

PGLAB_EBOARD_PARAMETERS = Schema (
    { 
        CONFIG_PARAMETERS: 
        {
            CONFIG_EBOARD_SHUTTERS: cv.shutter,
            CONFIG_EBOARD_BOARDS: cv.boards,
        }
    },
    required=True,
    extra=REMOVE_EXTRA,
)

class Device:
    """The class represent a generic PG LAB device."""

    def __init__(self) -> None:
        """Initiliaze."""

        # device ip address
        self._ip = None

        # the device mac address
        self._mac = None

        # device unique id along all PG Lab devices
        self._id = None

        # device friendly name for mqtt connection
        self._name = None

        # device name type
        self._type = None

        # the manufactor of the device
        self._manufacturer = None

        # the hardware version
        self._hardware_version = None

        # the firmware version
        self._firmware_version = None

        # specific parameters of the device
        self._parameters = None

        # prepare an array of available relays
        self._relays = []

        # prepare an array of available shutters
        self._shutters = []

        # prepare the sensors of the device
        self._sensors = None

        # internal configuration hash
        self._hash = hash(
            (
                self._id,
                self._name,
            )
        )

    async def config(self, mqtt: Client, config: dict, subscribe:bool = False) -> bool:
        """Perform internal configuration."""

        # validate config message
        try:
            config = PGLAB_DISCOVERY_SCHEMA(config)
        except MultipleInvalid as e:
            LOGGER.warning("Invalid discovey message (%s)", e)
            return False

        self._mac = config[CONFIG_MAC]
        self._ip = config[CONFIG_IP]
        self._id = config[CONFIG_ID]
        self._name = config[CONFIG_NAME]
        self._type = config[CONFIG_TYPE]
        self._manufacturer = config[CONFIG_MANUFACTOR]
        self._hardware_version = config[CONFIG_HARDWARE_VERSION]
        self._firmware_version = config[CONFIG_FIRMWARE_VERSION]

        # update the device hash
        self._hash = hash((self._id, self._name, self._mac))

        # initialize the specific type of device
        if self.is_eboard:

            # validate e-board parameters
            try:
                eboard_config = PGLAB_EBOARD_PARAMETERS(config)                
            except MultipleInvalid as e:
                LOGGER.warning("Invalid E-Board parameters message (%s)", e)
                return False

            # save the e-board parameters
            self._parameters = eboard_config[CONFIG_PARAMETERS]

            # update the device hash with specific e-board configuration
            self._hash = hash(
                (
                    self._hash,
                    self._parameters.get(CONFIG_EBOARD_SHUTTERS),
                    self._parameters.get(CONFIG_EBOARD_BOARDS),
                )
            )

            shutters = self._parameters.get(CONFIG_EBOARD_SHUTTERS)

            # prepare all shutters
            for index in range(0, shutters):
                if await self.is_relay_connected(index * 2):
                    shutter = await CreateShutter(self._id, self._name, index, mqtt)
                    if subscribe:
                        await shutter.subscribe_topics()
                    self._shutters.append(shutter)

            # prepare all relays
            for index in range(2 * shutters, 64):
                if await self.is_relay_connected(index):
                    relay = await CreateRelay(self._id, self._name, index, mqtt)
                    if subscribe:
                        await relay.subscribe_topics()
                    self._relays.append(relay)

            # prepare the sensor
            self._sensors = await CreateSensor(
                self._id, self._name, SENSOR_CONFIG[self._type], mqtt
            )
            
            if subscribe:
                await self._sensors.subscribe_topics()
        
        return True

    async def is_relay_connected(self, index):
        """Return if a specific relay is connected to e-board and available to use."""
        if self.is_eboard:
            if index < 0 or index > 63:
                return False

            boards = self._parameters[CONFIG_EBOARD_BOARDS]
            bi = index // 8

            return boards[bi] == "1"
        else:
            return False
        
    @property
    def is_eboard(self):
        """Return true if it is a E-Board device."""
        return self.type == PGLAB_DEVICE_TYPES[E_BOARD]

    @property
    def is_eswitch(self):
        """Return true if it is a E-Switch device."""
        return self.type == PGLAB_DEVICE_TYPES[E_SWITCH]

    @property
    def relays(self):
        """Get the relay array."""
        return self._relays

    @property
    def shutters(self):
        """Get the shutter array."""
        return self._shutters

    @property
    def sensors(self):
        """Get the device sensors ."""
        return self._sensors

    @property
    def ip(self) -> str:
        """Device ip."""
        return cast(str, self._ip)

    @property
    def mac(self) -> str:
        """Device mac."""
        return cast(str, self._mac)

    @property
    def id(self) -> str:
        """Device unique id."""
        return cast(str, self._id)

    @property
    def name(self) -> str:
        """Device friendly name."""
        return cast(str, self._name)

    @property
    def type(self) -> str:
        """Device type name (E-Board, E-Switch etc...)."""
        return cast(str, self._type)

    @property
    def manufactor(self) -> str:
        """Device manufacturer."""
        return cast(str, self._manufacturer)

    @property
    def hardware_version(self) -> str:
        """Device hardware version."""
        return cast(str, self._hardware_version)

    @property
    def firmware_version(self) -> str:
        """Device firmware version."""
        return cast(str, self._firmware_version)

    @property
    def hash(self) -> int:
        """Return device HASH."""
        return cast(int, self._hash)
