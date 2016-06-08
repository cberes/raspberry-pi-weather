class CelsiusTemperature(object):
    def __init__(self, value):
        self.__celsius = value

    def convert_to(self, unit):
        if unit == 'celsius':
            return (self.__celsius, '°C')
        elif unit == 'fahrenheit':
            return (self.__celsius * 9 / 5 + 32, '°F')
        else:
            raise NotImplementedError('cannot convert from celsius to ' + unit)

def celsius(value):
    return CelsiusTemperature(value)
