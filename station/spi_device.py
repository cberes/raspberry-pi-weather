from spidev import SpiDev
from contextlib import contextmanager

class SpiDevice:
    def __init__(self, bus, device):
        self.spi = SpiDev()
        self.spi.open(bus, device)

    def transfer(self, bytes):
        return self.spi.xfer2(bytes)

    def close(self):
        self.spi.close()

@contextmanager
def open_spi(bus, device):
    device = SpiDevice(bus, device)
    try:
        yield device
    finally:
        device.close()
