import PyDHT

from station.measurement import Measurement
from station.sensor_error import SensorError
from station.temperature import celsius

class HumiditySensor(object):
    def __init__(self, channel, **kwargs):
        self.channel = channel
        self.type = PyDHT.DHT22
        self.delay = 500
        self.temp_units = kwargs['temp_units'] if 'temp_units' in kwargs else 'celsius'

    def read(self):
        reading = PyDHT.read(self.type, self.channel, self.delay)
        if reading is None:
            raise SensorError('Humidity reading failed.')
        temperature, humidity = reading
        temperature = celsius(temperature).convert_to(self.temp_units)
        return (
            Measurement(name='humidity', abbrev='hum', value=humidity, units='%'),
            Measurement(name='temperature', abbrev='tmp', value=temperature[0],
                        units=temperature[1]),
        )

    @staticmethod
    def hw_init():
        PyDHT.init()

    @staticmethod
    def hw_close():
        PyDHT.close()
