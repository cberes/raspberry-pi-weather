class CelsiusTemperature(object):
    def __init__(self, value):
        self.__celsius = value
        self.__units = '°C'

    def to_celsius(self):
        return self.__celsius

    def to_fahrenheit(self):
        return self.__celsius * 9 / 5 + 32

    def get_value(self):
        return self.__celsius

    def get_units(self):
        return self.__units

class FahrenheitTemperature(object):
    def __init__(self, value):
        self.__fahrenheit = value
        self.__units = '°F'

    def to_celsius(self):
        return (self.__fahrenheit - 32) * 5 / 9

    def to_fahrenheit(self):
        return self.__fahrenheit

    def get_value(self):
        return self.__fahrenheit

    def get_units(self):
        return self.__units

def celsius(value):
    return CelsiusTemperature(value)

def fahrenheit(value):
    return FahrenheitTemperature(value)
