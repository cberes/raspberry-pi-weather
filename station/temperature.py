class CelsiusTemperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def to_celsius(self):
        return self.celsius

    def to_fahrenheit(self):
        return self.celsius * 9 / 5 + 32

class FahrenheitTemperature:
    def __init__(self, fahrenheit):
        self.fahrenheit = fahrenheit

    def to_celsius(self):
        return (self.fahrenheit - 32) * 5 / 9

    def to_fahrenheit(self):
        return self.fahrenheit

def celsius(value):
    return CelsiusTemperature(value)

def fahrenheit(value):
    return FahrenheitTemperature(value)
