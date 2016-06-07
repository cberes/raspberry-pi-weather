class SpiSensor(object):
    def __init__(self, device, channel):
        self.device = device
        self.channel = channel

    def init(self):
        self.device.init()

    def close(self):
        self.device.close()

    def read(self):
        pass
