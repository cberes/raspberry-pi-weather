class LcdCharacter:
    def __init__(self, code, bitmap):
        self.code = code
        self.bitmap = bitmap

degree = LcdCharacter(0, (
    0b00000,
    0b01110,
    0b01010,
    0b01110,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
))
