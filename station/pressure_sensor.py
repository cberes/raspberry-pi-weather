from spi_device import SpiDevice
from pressure import pascals
from temperature import celsius

class PressureSensor:
    def __init__(self, device):
        self.device = device

    def read_temperature_calibration(self):
        self.temperature_calibration = [
            self.read_unsigned_short(0x88),
            self.read_signed_short(0x8A),
            self.read_signed_short(0x8C),
            ]

    def read_pressure_calibration(self):
        self.pressure_calibration = [
            self.read_unsigned_short(0x8E),
            self.read_signed_short(0x90),
            self.read_signed_short(0x92),
            self.read_signed_short(0x94),
            self.read_signed_short(0x96),
            self.read_signed_short(0x98),
            self.read_signed_short(0x9A),
            self.read_signed_short(0x9C),
            self.read_signed_short(0x9E),
            ]

    def read(self):
        self.start()
        registers = self.read_registers(247, 6)
        temperature_reading = self.registers_to_data(registers, 3)
        t_fine, temperature = self.read_temperature(temperature_reading)
        pressure_reading = self.registers_to_data(registers, 0)
        pressure = self.read_pressure(t_fine, pressure_reading)
        return (pascals(pressure / 256), celsius(temperature / 100))

    def start(self):
        # send config and control registers
        self.device.transfer([117, 0, 116, 37])

    def read_registers(self, reg, n):
        # first byte can be ignored
        data = self.device.transfer([reg] + [0] * n)
        return data[1:]

    def registers_to_data(self, bytes, offset):
        return ((bytes[0 + offset] << 16) | (bytes[1 + offset] << 8) | bytes[2 + offset]) >> 4

    def read_temperature(self, temp):
        cal = self.temperature_calibration
        var1 = ((((temp >> 3) - (cal[0] << 1))) * cal[1]) >> 11
        var2 = (((((temp >> 4) - cal[0]) * ((temp >> 4) - cal[0])) >> 12) * cal[2]) >> 14
        t_fine = var1 + var2
        return (t_fine, (t_fine * 5 + 128) >> 8)

    def read_pressure(self, t_fine, pres):
        cal = self.pressure_calibration
        var1 = t_fine - 128000
        var2 = var1 * var1 * cal[5]
        var2 = var2 + ((var1 * cal[4]) << 17)
        var2 = var2 + (cal[3] << 35)
        var1 = ((var1 * var1 * cal[2]) >> 8) + ((var1 * cal[1]) << 12)
        var1 = (((1 << 47) + var1)) * cal[0] >> 33
        if var1 == 0:
        	return 0
        p = 1048576 - pres
        p = (((p << 31) - var2) * 3125) // var1
        var1 = (cal[8] * (p >> 13) * (p >> 13)) >> 25
        var2 = (cal[7] * p) >> 19
        return ((p + var1 + var2) >> 8) + (cal[6] << 4)

    def read_signed_short(self, reg):
        uns = self.read_unsigned_short(reg)
        return uns if uns < 32768 else (uns - 65536)

    def read_unsigned_short(self, reg):
        data = self.read_registers(reg, 2)
        return data[0] | (data[1] << 8)
