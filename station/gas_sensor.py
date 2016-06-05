class GasSensor(object):
    def __init__(self, read_channel, circuit):
        self.read_channel = read_channel
        self.circuit = circuit

    def read(self):
        voltage = self.read_channel()
        return self.circuit.get_resistance(voltage)
