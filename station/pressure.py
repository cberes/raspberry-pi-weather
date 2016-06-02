class Pascals(object):
    def __init__(self, value):
        self.__pascals = value

    def to_pascals(self):
        return self.__pascals

    def to_kilopascals(self):
        return self.__pascals / 1000

    def to_millibars(self):
        return self.__pascals / 100

    def to_inhg(self):
        return self.__pascals * 0.0002953

def pascals(value):
    return Pascals(value)
