import logging
from time import sleep

from pyPGLab import pyPGLab
from pyPGLab.hub import Hub

#logging.basicConfig(level=logging.DEBUG)

PG = pyPGLab()
PG.discover()

hub = Hub(PG.hubs[0])

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
shutter0 = hub.create_shutter(0)

relay4 = hub.create_relay(4)
relay5 = hub.create_relay(5)

shutter0.open()
sleep(2)
shutter0.close()

for i in range(20):
    if (i%2) == 1:
        relay4.turn_on()
        sleep(1)
        relay5.turn_off()        
        sleep(1)
    else:
        relay4.turn_off()
        sleep(1)
        relay5.turn_on()
        sleep(1)


#shutter0.close()

#import requests
#import json
#
#url = "http://" + hub + "/rpc.cgi"
#headers = {'Content-type': 'application/json', 'Accept': 'text/plain' }
#
#message = "cmd=id"
#
#x = requests.post(url, data = message,  headers=headers)
#
#reply = json.loads(x.text)
#print(reply["name"])
