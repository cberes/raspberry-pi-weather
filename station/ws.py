from time import sleep
from functools import partial

from station.lcd_output import open_lcd
from station.lcd_characters import DEGREE
from station.spi_device import open_spi
from station.adc_sensor import AdcSensor
from station.gas_sensor import GasSensor
from station.light_sensor import LightSensor
from station.temperature_sensor import TemperatureSensor
from station.pressure_sensor import PressureSensor
from station.humidity_sensor import HumiditySensor

def fmt(value):
    return str(round(value, 2))

def run_once(lcd, delay):
    # MCP3008 devices
    with open_spi(0, 0) as spi:
        adc = AdcSensor(spi, 3.3)
        light_sensor = LightSensor(partial(adc.voltage, 0))
        light = light_sensor.read()
        lcd.update("LIT: " + fmt(light.to_percent()) + "%")
        sleep(delay)
        gas_sensor = GasSensor(partial(adc.voltage, 1))
        air = gas_sensor.read()
        lcd.update("AIR: " + fmt(air.to_percent()) + "%")
        sleep(delay)
        temp_sensor = TemperatureSensor(partial(adc.voltage, 2))
        temp = temp_sensor.read()
        lcd.update("TMP: " + fmt(temp.to_celsius()) + chr(DEGREE.code) + "C, " +
                   fmt(temp.to_fahrenheit()) + chr(DEGREE.code) + "F")
        sleep(delay)

    # BMP280
    with open_spi(0, 1) as spi:
        pres_sensor = PressureSensor(spi)
        pres_sensor.read_temperature_calibration()
        pres_sensor.read_pressure_calibration()
        pressure, temp = pres_sensor.read()
        lcd.update("PRS: " + fmt(pressure.to_millibars()) + "hPa, " +
                   fmt(pressure.to_inhg()) + "inHg")
        sleep(delay)
        lcd.update("TMP: " + fmt(temp.to_celsius()) + chr(DEGREE.code) + "C, " +
                   fmt(temp.to_fahrenheit()) + chr(DEGREE.code) + "F")
        sleep(delay)

    # DHT22
    try:
        humidity_sensor = HumiditySensor(8)
        humidity, temp = humidity_sensor.read()
        lcd.update("HUM: " + fmt(humidity))
        sleep(delay)
        lcd.update("TMP: " + fmt(temp.to_celsius()) + chr(DEGREE.code) + "C, " +
                   fmt(temp.to_fahrenheit()) + chr(DEGREE.code) + "F")
        sleep(delay)
    except Exception as e:
        print(e)

def main():
    with open_lcd() as lcd:
        lcd.create(DEGREE)
        while True:
            run_once(lcd, 5)

if __name__ == '__main__':
    main()
