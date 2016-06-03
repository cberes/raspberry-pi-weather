from time import time
from station.digital_io import DigitalIO

class HumiditySensor(object):
    def __init__(self, channel):
        self.channel = DigitalIO(channel)

    def read(self):
        self.__start()
        return self.__read()

    def __start(self):
        self.channel.setup_out()
        self.channel.write(False)
        DigitalIO.usleep(500)
        self.channel.write(True)
        DigitalIO.usleep(10)
        self.channel.setup_in()
        self.channel.wait_for_falling()
        self.channel.wait_for_rising()
        self.channel.wait_for_falling()

    def __read(self):
        reading = HumidityReading()
        while not reading.is_done():
            reading.append(self.__read_bit())
        if not reading.is_valid():
            raise Exception('checksum failure')
        return reading.get()

    def __read_bit(self):
        self.channel.wait_for_rising()
        start = time()
        self.channel.wait_for_falling()
        end = time()
        return 0 if end - start < 5E-5 else 1

class HumidityReading(object):
    def __init__(self):
        self.data = 0
        self.bit_count = 0

    def append(self, datum):
        self.data = (self.data << 1) | datum
        self.bit_count += 1

    def is_valid(self):
        if not self.is_done():
            return False
        checksum = 0xFF & self.data
        data_bytes = self.__get_bytes()
        return (sum(data_bytes) & 0xFF) == checksum

    def is_done(self):
        return self.bit_count == 40

    def __get_bytes(self):
        return [
            0xFF & (self.data >> 32),
            0xFF & (self.data >> 24),
            0xFF & (self.data >> 16),
            0xFF & (self.data >> 8),
            ]

    def get(self):
        data_bytes = self.__get_bytes()
        humidity = HumidityReading.__combine_bytes(data_bytes, 0)
        temperature = HumidityReading.__combine_bytes(data_bytes, 2)
        return (humidity, temperature)

    @staticmethod
    def __combine_bytes(data_bytes, offset):
        integral = data_bytes[offset]
        signed_integral = integral if integral < 128 else (integral - 256)
        fractional = data_bytes[1 + offset]
        return ((signed_integral << 8) | fractional) / 100
