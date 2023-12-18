
class Relay:
    def __init__(self, hub, id):
        self.hub = hub
        self.relay_id = id

    def turn_on(self):
        self.hub.send_command("/relay/" + str(self.relay_id) + "/set/ON")

    def turn_off(self):
        self.hub.send_command("/relay/" + str(self.relay_id) + "/set/OFF")

    def auto_off(self, time_sec):
        self.hub.send_command("/relay/" + str(self.relay_id) + "/autoff/set/" + str(time_sec))
