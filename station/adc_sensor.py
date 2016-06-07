class AdcSensor(object):
    def __init__(self, device, channel, ref_voltage):
        self.device = device
        self.channel = channel
        self.ref_voltage = ref_voltage

    def init(self):
        self.device.init()

    def close(self):
        self.device.close()

    def voltage(self):
        value = self.read()
        return (value * self.ref_voltage) / 1024

    def read(self):
        data = self.device.transfer([1, (self.channel + 8) << 4, 0])
        return ((data[1] << 8) | data[2]) & 0x3FF
