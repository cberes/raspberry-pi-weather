class GasSensor(object):
    def __init__(self):
        self.read_channel = read_channel

    def read(self):
        return self.read_channel()
