import logging
from time import sleep

from pyPGLab import pyPGLab
from pyPGLab.device import Device

import requests
import json


def PrintHubInfo(device):
    if device is not None:
        print(f"IP : ({device.ip})")
        print(f"MAC : ({device.mac})")
        print(f"Unique ID : ({device.id})")
        print(f"Friendly name : ({device.name})")
        print(f"Type : ({device.type})")
        print(f"Manufactor : ({device.manufactor})")
        print(f"Hardware Version : ({device.hardware_version})")
        print(f"Firmware Version : ({device.firmware_version})")
    else:
        print ("PG LAB device not availabe")


PG = pyPGLab()
PG.discover()
device = PG.devices[0]

#device = Device("192.168.1.16")

PrintHubInfo(device)

for r in device.relays:
    r.toggle()

#print(hub.is_relay_connected(1))

# set the mqtt connection
#hub.mqtt("192.168.1.8")

# set the device name
#hub.device_name("eboard")

# set the default time to open or close a shutter
#hub.shutter_time(10, 30)

# set the number of shutter managed
#hub.shutter_count(2)

# flush all changes to the internal eeprom
#hub.flush_to_eeprom()

# reboot
#hub.reboot()

# wait a little until ebord is rebooting
#sleep(10)

# rebuild the hub
#hub = Hub(PG.hubs[0])

# change relay status
#relay0 = hub.create_relay(0)
#relay0.turn_on()

# change shutter status
#shutter0 = hub.create_shutter(0)

#relay4 = hub.create_relay(4)
#relay5 = hub.create_relay(5)

#shutter0.open()
#sleep(2)
#shutter0.close()

#for i in range(20):
#    if (i%2) == 1:
#        relay4.turn_on()
#        sleep(1)
#        relay5.turn_off()        
#        sleep(1)
#    else:
#        relay4.turn_off()
#        sleep(1)
#        relay5.turn_on()
#        sleep(1)
