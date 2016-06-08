from station.sensor import Sensor

class SpiSensor(Sensor):
    def __init__(self, device):
        super().__init__()
        self.device = device

    def init(self):
        self.device.init()

    def close(self):
        self.device.close()
