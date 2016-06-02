class LcdCharacter(object):
    def __init__(self, code, bitmap):
        self.code = code
        self.bitmap = bitmap

DEGREE = LcdCharacter(0, (
    0b00110,
    0b01001,
    0b01001,
    0b00110,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
))
