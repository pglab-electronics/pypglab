import json

class Relay:
    def __init__(self, device, id):
        self._device = device
        self._id = id

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def device(self):
        return self._device

    @property 
    def status(self) -> int:
        # querry the relay status
        res = self._device.send_command("/relay/" + str(self._id) + "/status")
        if res:
            # get device id info
            reply = json.loads(res.text)
            try:
                s = reply["status"]
                if s == '0':
                    # the relay is off 
                    return 0
                elif s == '1':
                    # the relay is on
                    return 1
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
        
    def toggle(self):
        s = self.status
        if s == 1:
            self.turn_off()
        elif s == 0:
            self.turn_on() 

    def turn_on(self):
        self._device.send_command("/relay/" + str(self._id) + "/set/ON")

    def turn_off(self):
        self._device.send_command("/relay/" + str(self._id) + "/set/OFF")

    def auto_off(self, time_sec):
        self._device.send_command("/relay/" + str(self._id) + "/autoff/set/" + str(time_sec))
