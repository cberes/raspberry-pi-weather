from time import sleep
from functools import partial

from lcd_output import open_lcd
from spi_device import open_spi
from adc_sensor import AdcSensor
from light_sensor import LightSensor
from temperature_sensor import TemperatureSensor
from pressure_sensor import PressureSensor

def fmt(value):
    return str(round(value, 2))

def run_once(lcd, delay):
    with open_spi(0, 0) as spi:
        adc = AdcSensor(spi, 3.3)
        ls = LightSensor(partial(adc.voltage, 0))
        light = ls.read()
        lcd.update("LI: " + fmt(light.to_percent()) + "%")
        sleep(delay)
        ts = TemperatureSensor(partial(adc.voltage, 2))
        temp = ts.read()
        lcd.update("TE: " + fmt(temp.to_celsius()) + "*C, " + fmt(temp.to_fahrenheit()) + "*F")
        sleep(delay)

    with open_spi(0, 1) as spi:
        ps = PressureSensor(spi)
        ps.read_temperature_calibration()
        ps.read_pressure_calibration()
        pressure, temp = ps.read()
        lcd.update("PR: " + fmt(pressure.to_millibars()) + "hPa, " + fmt(pressure.to_inhg()) + "inHg")
        sleep(delay)
        lcd.update("TE: " + fmt(temp.to_celsius()) + "*C, " + fmt(temp.to_fahrenheit()) + "*F")
        sleep(delay)

if __name__ == '__main__':
    with open_lcd() as lcd:
        while True:
            run_once(lcd, 5)
