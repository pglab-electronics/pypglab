
# pyPgLab

Library for PGLab smart home devices.

This library was created for PgLab devices for Home Assistant integrations.

## Features

- Discover devices
- Monitor status
- Monitor switch status
- Control (turn on/off etc)
- MQTT Server (buildin MQTT server that devices can connect to directly)
- MQTT Client (using a MQTT broker)
- Websocket
- Run only locally
- Support user name and password
- Support static and dynamic ip address
- mDns and MQTT discovery
- RPC (gen 2 devices)

## Devices supported

### Devices
- E-Board 

### Comming soon
- E-Switch

## Usage

```python
from pyPgLab import pyPgLab

def device_added(dev,code):
  print (dev," ",code)

pglab = pyPgLab()
print("version:",pglab.version())

pglab.cb_device_added.append(device_added)
pglab.start()
pglab.discover()

while True:
    pass 
```

## Feedback

Please give us feedback on pglab.electronics@gmail.com

## Founder

This plugin is created by PG Lab Electronics.

