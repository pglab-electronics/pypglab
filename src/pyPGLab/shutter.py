import json

class Shutter:
    def __init__(self, device, id):
        self._device = device
        self._id = id

    @property
    def id(self):
        return self._id
    
    @property
    def device(self):
        return self._device
    
    @property
    def status(self):
        # querry the shutter status
        res = self._device.send_command("/shutter/" + str(self._id) + "/status")
        if res:
            reply = json.loads(res.text)
            try:
                s = reply["status"]
                if s == '0':
                    # the shutter is in pause
                    return 0
                elif s == '1':
                    # the relay is opening
                    return 1
                elif s == '2':
                    # the relay is closing
                    return 2                
                else:
                    # the status has unexpeted value...
                    return -1
                
            except Exception as ex:
                # some thing bad happend ...
                return -1
        else:
            # for some reason it's not possible to querry the relay status
            # just return -1
            return -1

    def open(self):
        self._device.send_command("/shutter/" + str(self._id) + "/set/OPEN")

    def close(self):
        self._device.send_command("/shutter/" + str(self._id) + "/set/CLOSE")

    def stop(self):
        self._device.send_command("/shutter/" + str(self._id) + "/set/STOP")

    def timing(self, opening, closing):
        self._device.send_command("/shutter/" + str(self._id) + "/set/CLOSE")

