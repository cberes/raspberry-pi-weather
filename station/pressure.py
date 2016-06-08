class Pascals(object):
    def __init__(self, value):
        self.__pascals = value

    def convert_to(self, unit):
        if unit == 'pascals':
            return (self.__pascals, 'Pa')
        elif unit == 'kilopascals':
            return (self.__pascals / 1000, 'KPa')
        elif unit == 'millibars':
            return (self.__pascals / 100, 'hPa')
        elif unit == 'inhg':
            return (self.__pascals * 0.0002953, 'inHg')
        else:
            raise NotImplementedError('cannot convert from pascals to ' + unit)

def pascals(value):
    return Pascals(value)
