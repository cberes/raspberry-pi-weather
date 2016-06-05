from station.temperature import celsius

class TemperatureSensor(object):
    def __init__(self, read_channel):
        self.read_channel = read_channel

    def read(self):
        voltage = self.read_channel()
        temperature = (voltage - 0.5) * 100
        return celsius(temperature)
