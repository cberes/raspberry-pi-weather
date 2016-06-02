from time import sleep
from functools import partial

from station.lcd_output import open_lcd
from station.lcd_characters import DEGREE
from station.spi_device import open_spi
from station.adc_sensor import AdcSensor
from station.light_sensor import LightSensor
from station.temperature_sensor import TemperatureSensor
from station.pressure_sensor import PressureSensor

def fmt(value):
    return str(round(value, 2))

def run_once(lcd, delay):
    with open_spi(0, 0) as spi:
        adc = AdcSensor(spi, 3.3)
        light_sensor = LightSensor(partial(adc.voltage, 0))
        light = light_sensor.read()
        lcd.update("LI: " + fmt(light.to_percent()) + "%")
        sleep(delay)
        temp_sensor = TemperatureSensor(partial(adc.voltage, 2))
        temp = temp_sensor.read()
        lcd.update("TE: " + fmt(temp.to_celsius()) + chr(DEGREE.code) + "C, " +
                   fmt(temp.to_fahrenheit()) + chr(DEGREE.code) + "F")
        sleep(delay)

    with open_spi(0, 1) as spi:
        pres_sensor = PressureSensor(spi)
        pres_sensor.read_temperature_calibration()
        pres_sensor.read_pressure_calibration()
        pressure, temp = pres_sensor.read()
        lcd.update("PR: " + fmt(pressure.to_millibars()) + "hPa, " +
                   fmt(pressure.to_inhg()) + "inHg")
        sleep(delay)
        lcd.update("TE: " + fmt(temp.to_celsius()) + chr(DEGREE.code) + "C, " +
                   fmt(temp.to_fahrenheit()) + chr(DEGREE.code) + "F")
        sleep(delay)

def main():
    with open_lcd() as lcd:
        lcd.create(DEGREE)
        while True:
            run_once(lcd, 5)

if __name__ == '__main__':
    main()

