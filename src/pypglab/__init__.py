#import PGLab modules
from .const import VERSION, PGLAB_MDNS_HTTP_SERVER, LOGGER
from .device import Device

#import all other modules
from time import sleep
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf,DNSAddress
from typing import cast

class pyPGLab():
    
    def __init__(self):
        self._version = VERSION
        self._devices = []

    def __on_service_state_change(self, zeroconf, service_type, name, state_change):
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info :
                if info.name == PGLAB_MDNS_HTTP_SERVER:
                    
                    # we found a PG LAB device ... save the IP address
                    addrs = info.parsed_scoped_addresses()

                    if addrs:
                        # add IP4 address to the PGLAB devices
                        device = Device(addrs[0])
                        self._devices.append(device)

    @property
    def version(self):
        return self._version

    @property
    def devices(self):
        return self._devices

    def discover(self):
        #clear all devices
        self._devices.clear()

        #looking for http mDNS service
        zeroconf = Zeroconf()
        ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[self.__on_service_state_change])
        sleep(2)

        LOGGER.warning("Found %d devices", len(self._devices) )

        zeroconf.close()
        

