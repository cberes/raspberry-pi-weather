class CelsiusTemperature(object):
    def __init__(self, value):
        self.__celsius = value

    def to_celsius(self):
        return self.__celsius

    def to_fahrenheit(self):
        return self.__celsius * 9 / 5 + 32

class FahrenheitTemperature(object):
    def __init__(self, value):
        self.__fahrenheit = value

    def to_celsius(self):
        return (self.__fahrenheit - 32) * 5 / 9

    def to_fahrenheit(self):
        return self.__fahrenheit

def celsius(value):
    return CelsiusTemperature(value)

def fahrenheit(value):
    return FahrenheitTemperature(value)
