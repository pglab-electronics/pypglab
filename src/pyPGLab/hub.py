from .const import LOGGER, PGLAB_DEVICE_TYPES
from .relay import Relay
from .shutter import Shutter


import requests
import json

class Hub():
    def __init__(self, ip_addr):
        self.ip = ip_addr
        self.id = None
        self.mac = None
        self.type = None
        self.name = None
        self.ver = None
        self.firmware = None
        self.parameters = None

        # get the PGLab device information
        res = self.send_command("/system/id")

        LOGGER.info("rpc system id: %s", res.text)

        # fill informations about the device
        # all PG LAB device have to reply properly
        if res:
            reply = json.loads(res.text)

            try:
                self.id = reply["id"]
                self.mac = reply["mac"]
                self.type = reply["type"]
                self.name = reply["name"]
                self.ver = reply["ver"]
            except Exception as ex:
                LOGGER.error("Error, missing field(%s)", ex)
        else:
                LOGGER.error("No Reply from RPC call to (%s)", self.ip)

        # get specific configuration for E-Board
        if self.type == PGLAB_DEVICE_TYPES['E-BOARD']['name']:
            try:
                res = self.send_command("/system/parameters")
                self.parameters  = json.loads(res.text)
            except Exception as ex:
                LOGGER.error("Error, getting configuration from E-Board device (%s)", ex)


        # get specific configuration fro E-SWITCH
        #if self.type == PGLAB_DEVICE_TYPES['E-SWITCH']['name']:
        #    # get the device parameters
        #    res = self.send_command("/system/parameters")

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