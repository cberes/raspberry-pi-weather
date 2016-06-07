import PyDHT

from station.measurement import Measurement
from station.sensor_error import SensorError
from station.temperature import celsius

class HumiditySensor(object):
    def __init__(self, channel, **kwargs):
        self.channel = channel
        self.type = PyDHT.DHT22
        self.delay = 500
        self.fahrenheit = 'fahrenheit' in kwargs and kwargs['fahrenheit']

    def init(self):
        PyDHT.init()

    def read(self):
        reading = PyDHT.read(self.type, self.channel, self.delay)
        if reading is None:
            raise SensorError('Humidity reading failed.')
        temperature, humidity = reading
        celsius_temp = celsius(temperature)
        temp_in_desired_units = celsius_temp.to_fahrenheit() if self.fahrenheit else celsius_temp
        return (
            Measurement(name='humidity', abbrev='hum', value=humidity, units='%'),
            Measurement(name='temperature', abbrev='tmp', value=temp_in_desired_units.get_value(),
                        units=temp_in_desired_units.get_units()),
        )

    def close(self):
        PyDHT.close()
