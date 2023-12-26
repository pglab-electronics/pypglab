import logging

LOGGER = logging.getLogger('pyPGLab')

NAME = "pyPgLab"
VERSION = "1.0.1"

PGLAB_DEVICE_TYPES = {
    'E-BOARD': {'name': "E-Board", 'mqtt':'eboard'},
    'E-RELAY': {'name': "E-Relay", 'mqtt':'erealy'},
    'E-SWITCH': {'name': "E-Switch", 'mqtt':'eswitch'},
}

PGLAB_MDNS_HTTP_SERVER = "pglab._http._tcp.local."
