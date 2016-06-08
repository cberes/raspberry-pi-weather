class SpiSensor(object):
    def __init__(self, device):
        self.device = device

    def init(self):
        self.device.init()

    def close(self):
        self.device.close()

    def read(self):
        pass
