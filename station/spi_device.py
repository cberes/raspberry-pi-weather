from contextlib import contextmanager
from spidev import SpiDev

class SpiDevice(object):
    def __init__(self, bus, device):
        self.spi = SpiDev()
        self.bus = bus
        self.device = device

    def init(self):
        self.spi.open(self.bus, self.device)

    def transfer(self, data):
        return self.spi.xfer2(data)

    def close(self):
        self.spi.close()

@contextmanager
def open_spi(bus, device):
    device = SpiDevice(bus, device)
    try:
        yield device
    finally:
        device.close()
