#import PGLab modules
from .const import VERSION, PGLAB_MDNS_HTTP_SERVER, LOGGER

#import all other modules
from time import sleep
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf,DNSAddress
from typing import cast


class pyPGLab():
    def __init__(self):
        self.version = VERSION
        self.hubs = []

    def __on_service_state_change(self, zeroconf, service_type, name, state_change):
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info :
                if info.name == PGLAB_MDNS_HTTP_SERVER:
                    
                    # we found a PG LAB device ... save the IP address
                    addrs = info.parsed_scoped_addresses()

                    if addrs:
                        # add IP4 address to the PGLAB hubs                        
                        #print(addrs[0])
                        self.hubs.append(addrs[0])


    def get_version(self):
        return self.version

    def discover(self):

        #clear all hubs
        self.hubs.clear()

        #looking for http mDNS service
        zeroconf = Zeroconf()
        ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[self.__on_service_state_change])
        sleep(2)

        LOGGER.warning("Found %d hubs", len(self.hubs) )

        zeroconf.close()
        

