from station.voltage import Voltage

class AdcSensor(object):
    def __init__(self, device, ref_voltage):
        self.device = device
        self.ref_voltage = ref_voltage

    def voltage(self, channel):
        value = self.read(channel)
        voltage = (value * self.ref_voltage) / 1024
        return Voltage(voltage, self.ref_voltage)

    def read(self, channel):
        data = self.device.transfer([1, (channel + 8) << 4, 0])
        return ((data[1] << 8) | data[2]) & 0x3FF
