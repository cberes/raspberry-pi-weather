class Voltage:
    def __init__(self, voltage, reference):
        self.voltage = voltage
        self.reference = reference

    def to_voltage(self):
        return self.voltage

    def to_percent(self):
        return ((self.reference - self.voltage) / self.reference) * 100
