from temperature import celsius

class TemperatureSensor:
    def __init__(self, read_channel):
        self.read_channel = read_channel

    def read(self):
        voltage = self.read_channel().voltage()
        temperature = (voltage - 0.5) * 100
        return celsius(temperature)
