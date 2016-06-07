from station.measurement import Measurement
from station.spi_sensor import SpiSensor
from station.temperature import celsius

class TemperatureSensor(SpiSensor):
    def __init__(self, device, **kwargs):
        super().__init__(device)
        self.fahrenheit = 'fahrenheit' in kwargs and kwargs['fahrenheit']

    def read(self):
        voltage = self.device.voltage()
        temperature = (voltage - 0.5) * 100
        celsius_temp = celsius(temperature)
        temp_in_desired_units = celsius_temp.to_fahrenheit() if self.fahrenheit else celsius_temp
        return (
            Measurement(name='temperature', abbrev='tmp', value=temp_in_desired_units.get_value(),
                        units=temp_in_desired_units.get_units()),
        )
