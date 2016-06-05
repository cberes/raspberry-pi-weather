from time import sleep
from functools import partial

from station.spi_device import open_spi
from station.adc_sensor import AdcSensor
from station.gas_sensor import GasSensor
from station.light_sensor import LightSensor
from station.temperature_sensor import TemperatureSensor
from station.pressure_sensor import PressureSensor
from station.humidity_sensor import HumiditySensor, open_dht
from station.circuits.voltage_load import VoltageLoad
from station.circuits.voltage_divider import VoltageDivider
from station.lcd.output import open_lcd
from station.lcd.characters import DEGREE, OHM

def fmt(value):
    return str(round(value, 2))

def print_temp(temp, lcd):
    lcd.update("TMP: " + fmt(temp.to_celsius()) + chr(DEGREE.code) + "C, " +
               fmt(temp.to_fahrenheit()) + chr(DEGREE.code) + "F")

def read_mcp3008(lcd, delay):
    with open_spi(0, 0) as spi:
        adc = AdcSensor(spi, 3.3)
        light_sensor = LightSensor(partial(adc.voltage, 0), VoltageLoad(3.3, 1000))
        light = light_sensor.read()
        lcd.update("LIT: " + fmt(light) + "lx")
        sleep(delay)
        gas_sensor = GasSensor(partial(adc.voltage, 1), VoltageDivider(5.0, 10000, 20000))
        air = gas_sensor.read()
        lcd.update("AIR: " + fmt(air) + chr(OHM.code))
        sleep(delay)
        temp_sensor = TemperatureSensor(partial(adc.voltage, 2))
        temp = temp_sensor.read()
        print_temp(temp, lcd)
        sleep(delay)

def read_bmp280(lcd, delay):
    with open_spi(0, 1) as spi:
        pres_sensor = PressureSensor(spi)
        pres_sensor.read_temperature_calibration()
        pres_sensor.read_pressure_calibration()
        pressure, temp = pres_sensor.read()
        lcd.update("PRS: " + fmt(pressure.to_millibars()) + "hPa, " +
                   fmt(pressure.to_inhg()) + "inHg")
        sleep(delay)
        print_temp(temp, lcd)
        sleep(delay)

def read_dht22(lcd, delay):
    with open_dht():
        humidity_sensor = HumiditySensor(14)
        humidity, temp = humidity_sensor.read()
        if humidity is not None and temp is not None:
            lcd.update("HUM: " + fmt(humidity) + "%")
            sleep(delay)
            print_temp(temp, lcd)
            sleep(delay)

def run_once(lcd, delay):
    read_mcp3008(lcd, delay)
    read_bmp280(lcd, delay)
    read_dht22(lcd, delay)

def main():
    with open_lcd() as lcd:
        lcd.create(DEGREE)
        lcd.create(OHM)
        while True:
            run_once(lcd, 5)

if __name__ == '__main__':
    main()
