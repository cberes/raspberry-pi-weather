PASCALS = 'pascals'
KILOPASCALS = 'kilopascals'
MILLIBARS = 'millibars'
IN_HG = 'inhg'

class Pascals(object):
    def __init__(self, value):
        self.__pascals = value

    def convert_to(self, unit):
        if unit == PASCALS:
            return (self.__pascals, 'Pa')
        elif unit == KILOPASCALS:
            return (self.__pascals / 1000, 'KPa')
        elif unit == MILLIBARS:
            return (self.__pascals / 100, 'hPa')
        elif unit == IN_HG:
            return (self.__pascals * 0.0002953, 'inHg')
        else:
            raise NotImplementedError('cannot convert from pascals to ' + unit)

def pascals(value):
    return Pascals(value)
