from time import sleep

from station.spi_device import SpiDevice
from station.adc_sensor import AdcSensor
from station.gas_sensor import GasSensor
from station.light_sensor import LightSensor
from station.temperature_sensor import TemperatureSensor
from station.pressure_sensor import PressureSensor
from station.humidity_sensor import HumiditySensor
from station.sensor_error import SensorError
from station.circuits.voltage_load import VoltageLoad
from station.circuits.voltage_divider import VoltageDivider
from station.lcd.output import LcdOutput
from station.lcd.characters import DEGREE, OHM

class WeatherStation(object):
    def __init__(self, lcd, delay):
        self.lcd = lcd
        self.delay = delay
        self.sensors = []

    def run_forever(self):
        try:
            self.__add_lcd_chars()
            self.__create_sensors()
            while True:
                self.__run_once()
        finally:
            self.lcd.close()

    def __add_lcd_chars(self):
        self.lcd.create(DEGREE)
        self.lcd.create(OHM)

    def __create_sensors(self):
        self.sensors += (
            LightSensor(AdcSensor(SpiDevice(0, 0), 0, 3.3), VoltageLoad(3.3, 1000)),
            GasSensor(AdcSensor(SpiDevice(0, 0), 1, 3.3), VoltageDivider(5.0, 10000, 20000)),
            TemperatureSensor(AdcSensor(SpiDevice(0, 0), 2, 3.3)),
            PressureSensor(SpiDevice(0, 1)),
            HumiditySensor(14),
        )

    def __run_once(self):
        for sensor in self.sensors:
            try:
                self.__read_sensor(sensor)
            except SensorError:
                self.lcd.update(type(sensor).__name__ + " failure!")
                sleep(self.delay)
            finally:
                sensor.close()

    def __read_sensor(self, sensor):
        sensor.init()
        for measurement in sensor.read():
            self.lcd.update(measurement.get_abbrev().upper() + ": " + \
                str(round(measurement.get_value(), 2)) + " " + measurement.get_units())
            sleep(self.delay)

if __name__ == '__main__':
    WeatherStation(LcdOutput(), 5).run_forever()
