from contextlib import contextmanager
import PyDHT

from station.temperature import celsius

class HumiditySensor(object):
    def __init__(self, channel):
        self.channel = channel
        self.type = PyDHT.DHT22
        self.delay = 500

    def read(self):
        reading = PyDHT.read(self.type, self.channel, self.delay)
        if reading is None:
            return (None, None)
        temperature, humidity = reading
        return (humidity, celsius(temperature))

@contextmanager
def open_dht():
    PyDHT.init()
    try:
        yield
    finally:
        PyDHT.close()

