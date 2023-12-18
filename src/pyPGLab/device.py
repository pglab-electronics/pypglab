from .const import LOGGER

import requests

class Device():
    def __init__(self, ip_addr):
        self.ip = ip_addr

    def send_command(self, message):
        url = "http://" + self.ip + "/rpc.cgi"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain' }
        x = None
        try:
            x = requests.post(url, data = "cmd=" + message,  headers=headers)
        except Exception as ex:
            LOGGER.debug("Error look up name, %s", ex)
        return x