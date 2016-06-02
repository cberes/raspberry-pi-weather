from spidev import SpiDev
import time

from lcd_output import LcdOutput

def toVolts(value):
    return (value * 3.3) / 1024

def scaleVolts(value):
    return ((3.3 - value) / 3.3) * 100

def scaleTemp(value):
    return (value - 0.5) * 100

def c2f(c):
    return c * 9 / 5 + 32

def readMcp3008(spi, channel):
    adc = spi.xfer2([1, (channel + 8) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def readLightAndTemp(device):
    spi = SpiDev()
    spi.open(0, device)
    light = readMcp3008(spi, 0)
    temp = readMcp3008(spi, 2)
    spi.close()
    light, temp = list(map(toVolts, [light, temp]))
    return [scaleVolts(light), scaleTemp(temp)]

def configBmp280(spi):
    # send config and control registers
    spi.xfer2([117, 0, 116, 37])

def readBmp280(spi, reg, n):
    # first byte can be ignored
    adc = spi.xfer2([reg] + [0] * n)
    return adc[1:]

def bmp280Data(bytes):
    return ((bytes[0] << 16) | (bytes[1] << 8) | bytes[2]) >> 4

def readUnsignedShort(spi, reg):
    data = readBmp280(spi, reg, 2)
    return data[0] | (data[1] << 8)

def readSignedShort(spi, reg):
    uns = readUnsignedShort(spi, reg)
    return uns if uns < 32768 else (uns - 65536)

def tempCalibData(spi):
    return [readUnsignedShort(spi, 0x88),
            readSignedShort(spi, 0x8A),
            readSignedShort(spi, 0x8C)]

def calcTemp(temp, calib):
    var1 = ((((temp >> 3) - (calib[0] << 1))) * calib[1]) >> 11
    var2 = (((((temp >> 4) - calib[0]) * ((temp >> 4) - calib[0])) >> 12) * calib[2]) >> 14
    tFine = var1 + var2
    return [tFine, (tFine * 5 + 128) >> 8]

def pressureCalibData(spi):
    return [readUnsignedShort(spi, 0x8E),
            readSignedShort(spi, 0x90),
            readSignedShort(spi, 0x92),
            readSignedShort(spi, 0x94),
            readSignedShort(spi, 0x96),
            readSignedShort(spi, 0x98),
            readSignedShort(spi, 0x9A),
            readSignedShort(spi, 0x9C),
            readSignedShort(spi, 0x9E)]

def calcPressure(tFine, pres, calib):
    var1 = tFine - 128000
    var2 = var1 * var1 * calib[5]
    var2 = var2 + ((var1 * calib[4]) << 17)
    var2 = var2 + (calib[3] << 35)
    var1 = ((var1 * var1 * calib[2]) >> 8) + ((var1 * calib[1]) << 12)
    var1 = (((1 << 47) + var1)) * calib[0] >> 33
    if var1 == 0:
    	return 0
    p = 1048576 - pres
    p = (((p << 31) - var2) * 3125) // var1
    var1 = (calib[8] * (p >> 13) * (p >> 13)) >> 25
    var2 = (calib[7] * p) >> 19
    return ((p + var1 + var2) >> 8) + (calib[6] << 4)

def readTempAndPressure(device):
    spi = SpiDev()
    spi.open(0, device)
    configBmp280(spi)
    regs = readBmp280(spi, 247, 6)
    data = [regs[0:3], regs[3:6]]
    pres, temp = list(map(bmp280Data, data))
    tFine, tempCalib = calcTemp(temp, tempCalibData(spi))
    presCalib = calcPressure(tFine, pres, pressureCalibData(spi))
    spi.close()
    return [presCalib / 256, tempCalib / 100]

def s(value):
    return str(round(value, 2))

def runOnce(lcd, delay):
    light, temp = readLightAndTemp(0)
    lcd.update("LI: " + s(light) + "%")
    time.sleep(delay)
    lcd.update("TE: " + s(temp) + "*C, " + s(c2f(temp)) + "*F")
    time.sleep(delay)
    pressure, temp2 = readTempAndPressure(1)
    lcd.update("PR: " + s(pressure) + "Pa, " + s(pressure * 0.0002953) + "inHg")
    time.sleep(delay)
    lcd.update("TE: " + s(temp2) + "*C, " + s(c2f(temp2)) + "*F")
    time.sleep(delay)

lcd = LcdOutput()
try:
    while True:
        runOnce(lcd, 5)
finally:
    lcd.close()
exit()
