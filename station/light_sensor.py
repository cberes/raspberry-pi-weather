class LightSensor:
    def __init__(self, read_channel):
        self.read_channel = read_channel

    def read(self):
        return self.read_channel()
