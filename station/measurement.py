class Measurement(object):
    def __init__(self, **kwargs):
        self.value = kwargs['value']
        self.units = kwargs['units']
        self.name = kwargs['name']
        self.abbrev = kwargs['abbrev']

    def get_value(self):
        return self.value

    def get_units(self):
        return self.units

    def get_name(self):
        return self.name

    def get_abbrev(self):
        return self.abbrev
