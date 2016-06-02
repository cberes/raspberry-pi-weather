class Pascals:
    def __init__(self, pascals):
        self.pascals = pascals

    def to_pascals(self):
        return self.pascals

    def to_kilopascals(self):
        return self.pascals / 1000

    def to_millibars(self):
        return self.pascals / 100

    def to_inhg(self):
        return self.pascals * 0.0002953

def pascals(value):
    return Pascals(value)
