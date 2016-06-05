from functools import partial
from concurrent.futures import ThreadPoolExecutor, CancelledError

from station.spi_device import open_spi
from station.adc_sensor import AdcSensor
from station.gas_sensor import GasSensor
from station.light_sensor import LightSensor
from station.temperature_sensor import TemperatureSensor
from station.pressure_sensor import PressureSensor
from station.humidity_sensor import HumiditySensor, open_dht
from station.serial_display import SerialDisplay
from station.circuits.voltage_load import VoltageLoad
from station.circuits.voltage_divider import VoltageDivider
from station.lcd.output import open_lcd
from station.lcd.characters import DEGREE, OHM

def run_forever():
    delay = 5
    with open_lcd() as lcd, ThreadPoolExecutor(max_workers=1) as executor, open_dht():
        lcd.create(DEGREE)
        lcd.create(OHM)
        display = SerialDisplay(lcd, delay)
        while True:
            run_once(display, executor, delay)

def run_once(display, executor, delay):
    read_mcp3008(display)
    read_bmp280(display)
    read_dht22(display, executor, delay)

def format_temp(temp):
    return "TMP: " + fmt(temp.to_celsius()) + chr(DEGREE.code) + "C, " + \
           fmt(temp.to_fahrenheit()) + chr(DEGREE.code) + "F"

def fmt(value):
    return str(round(value, 2))

def read_mcp3008(display):
    with open_spi(0, 0) as spi:
        adc = AdcSensor(spi, 3.3)
        light_sensor = LightSensor(partial(adc.voltage, 0), VoltageLoad(3.3, 1000))
        light = light_sensor.read()
        display.update("LIT: " + fmt(light) + "lx")
        gas_sensor = GasSensor(partial(adc.voltage, 1), VoltageDivider(5.0, 10000, 20000))
        air = gas_sensor.read()
        display.update("AIR: " + fmt(air) + chr(OHM.code))
        temp_sensor = TemperatureSensor(partial(adc.voltage, 2))
        temp = temp_sensor.read()
        display.update(format_temp(temp))

def read_bmp280(display):
    with open_spi(0, 1) as spi:
        pres_sensor = PressureSensor(spi)
        pres_sensor.read_temperature_calibration()
        pres_sensor.read_pressure_calibration()
        pressure, temp = pres_sensor.read()
        display.update("PRS: " + fmt(pressure.to_millibars()) + "hPa, " +
                       fmt(pressure.to_inhg()) + "inHg")
        display.update(format_temp(temp))

def read_dht22(display, executor, delay):
    future = executor.submit(read_humidity, 14)
    try:
        humidity, temp = future.result(delay)
        print_humidity(display, humidity, temp)
    except (CancelledError, TimeoutError):
        future.cancel()
        display.update("Humidity reading failed!")

def read_humidity(pin):
    humidity_sensor = HumiditySensor(pin)
    return humidity_sensor.read()

def print_humidity(display, humidity, temp):
    if humidity is not None and temp is not None:
        display.update("HUM: " + fmt(humidity) + "%")
        display.update(format_temp(temp))
    else:
        display.update("No humidity reading!")

if __name__ == '__main__':
    run_forever()
