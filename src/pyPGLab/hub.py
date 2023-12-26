from .const import LOGGER, PGLAB_DEVICE_TYPES
from .relay import Relay
from .shutter import Shutter

from typing import cast

import requests
import json

class Hub():
    def __init__(self, ip_addr):
        # device ip address
        self._ip = ip_addr

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

        # get the PGLab device information
        res = self.send_command("/system/id")

        # fill informations about the device
        # all PG LAB devices have to reply
        if res:
            LOGGER.info("rpc system id: %s", res.text)

            # get device id info
            reply = json.loads(res.text)
            try:
                self._mac = reply["mac"]
                self._id = reply["id"]
                self._name = reply["name"]
                self._type = reply["type"]
                self._manufacturer = reply["manufacturer"]
                self._hardware_version = reply["hw_ver"]
                self._firmware_version = reply["fw_ver"]
            except Exception as ex:
                LOGGER.error("Error, missing field(%s)", ex)
            else:
                # get specific configuration of the device
                try:
                    res = self.send_command("/system/parameters")
                    self._parameters  = json.loads(res.text)
                except Exception as ex:
                    LOGGER.error("Error, getting parameters from the device (%s)", ex)
        else:
            LOGGER.error("No Reply from RPC call to (%s)", self.ip)

    def send_command(self, message):
        url = "http://" + self.ip + "/rpc.cgi"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain' }
        x = None
        try:
            x = requests.post(url, data = "cmd=" + message,  headers=headers)
        except Exception as ex:
            LOGGER.debug("Error look up name, %s", ex)
        return x
    
    def is_eboard(self):
        # return true if hus is a E-Board device
        return self.type == PGLAB_DEVICE_TYPES['E-BOARD']['name']
    
    def is_eswitch(self):
        return False
    
    def is_relay_connected(self, index):
        # return if a specific relay is connected to e-board and available to use
        if self.is_eboard():
            try:
                if index < int(self.parameters['relays_count']):
                    connection_status = self.parameters['relays_status']
                    status_mask = connection_status[ index / 8]
                    return status_mask & (1 << (index % 8))
                else:
                    # index out of range
                    return False
            except Exception as ex:
                LOGGER.debug("Error in getting if a relay is connected, %s", ex)

            return True
        else:
            return False
    
    def reboot(self):
        self.send_command("/system/reboot")

    def flush_to_eeprom(self):
        self.send_command("/system/flush_to_eeprom")

    def reset(self):
        self.send_command("/system/reset")

    def device_name(self, name):
        # set the device name, be sure to have an unique name alongh all available
        # device in the local network
        self.send_command("/system/name/" + name)

    def autoff(self, time_sec):
        # set the global time for turn off relay that is been activated        
        self.hub.send_command("/system/relays/autoff/" + str(time_sec))

    def mqtt(self, server, port=1883, login="", password=""):
        # set the mqtt server with loging and password
        # after the call is required to flush to eeprom and reboot the board
        self.send_command("/system/mqtt/server/" + server)
        self.send_command("/system/mqtt/port/" + str(port))
        self.send_command("/system/mqtt/username/" + login)
        self.send_command("/system/mqtt/password/" + password)

    def shutter_time(self, open_time, close_time):
        # set the global time for turn off relay that is been activated        
        self.send_command("/system/shutters/opentime/"  + str(open_time))
        self.send_command("/system/shutters/closetime/" + str(close_time))

    def shutter_count(self, count):
        # set the number of shutter that the hub can manage
        self.send_command("/system/shutters/count/" + str(count))

    def relay_count(self):
        # get the total number of relay controlled
        if self.is_eboard():
            return int(self.parameters['relays_count'])
        else:
            return 0
    
    def create_relay(self, index):
        # create a relay, only e-board can create a relay
        if self.is_eboard():
            try: 
                # shutter have priority... only create a relay with index that don't conflict with shutter
                if (index >= int(self.parameters['shutters_count'])) and (index < int(self.parameters['relays_count'])):
                    if self.is_relay_connected(index):
                        return Relay(self, index)
                return None
            except Exception as ex:
                LOGGER.error("Error in shutter creation, %s", ex)
        else:
            return None
    
    def create_shutter(self, index):
        # create a shutter, only e-board can create a shutter
        if self.is_eboard():
            try:
                if index < int(self.parameters['shutters_count']):
                    if self.is_relay_connected(index)*2:
                        return Shutter(self, index)                
                return None
            except Exception as ex:
                LOGGER.error("Error in shutter creation, %s", ex)
        else:
            return None
    
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
        """Device type name (E-Board, E-Switch etc...)"""
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