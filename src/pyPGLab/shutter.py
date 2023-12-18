
class Shutter:
    def __init__(self, hub, id):
        self.hub = hub
        self.shutter_id = id

    def open(self):
        self.hub.send_command("/shutter/" + str(self.shutter_id) + "/set/OPEN")

    def close(self):
        self.hub.send_command("/shutter/" + str(self.shutter_id) + "/set/CLOSE")

    def timing(self, opening, closing):
        self.hub.send_command("/shutter/" + str(self.shutter_id) + "/set/CLOSE")

