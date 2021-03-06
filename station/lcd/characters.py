class LcdCharacter(object):
    def __init__(self, code, replacement, bitmap):
        self.code = code
        self.replacement = replacement
        self.bitmap = bitmap

DEGREE = LcdCharacter(0, '°', (
    0b00110,
    0b01001,
    0b01001,
    0b00110,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
))

OHM = LcdCharacter(1, 'Ω', (
    0b00000,
    0b01110,
    0b10001,
    0b10001,
    0b10001,
    0b01010,
    0b11011,
    0b00000,
))
