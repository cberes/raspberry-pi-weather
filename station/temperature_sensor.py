from station.measurement import Measurement
from station.spi_sensor import SpiSensor
from station.temperature import celsius

class TemperatureSensor(SpiSensor):
    def __init__(self, device, **kwargs):
        super().__init__(device)
        self.temp_units = kwargs['temp_units'] if 'temp_units' in kwargs else 'celsius'

    def read(self):
        voltage = self.device.voltage()
        temperature = (voltage - 0.5) * 100
        temperature = celsius(temperature).convert_to(self.temp_units)
        return (
            Measurement(name='temperature', abbrev='tmp', value=temperature[0],
                        units=temperature[1]),
        )
