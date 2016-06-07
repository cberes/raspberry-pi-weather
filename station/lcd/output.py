from contextlib import contextmanager
import RPi.GPIO as GPIO
from RPLCD import CharLCD, cleared

class LcdOutput(object):
    def __init__(self):
        self.lcd = CharLCD(pin_rs=3, pin_e=5, pins_data=[18, 22, 7, 13],
                           pin_rw=None, numbering_mode=GPIO.BOARD,
                           cols=16, rows=2, dotsize=8)
        self.chars = {}

    def update(self, *lines):
        with cleared(self.lcd):
            for i in range(0, len(lines)):
                self.lcd.cursor_pos = (i, 0)
                text = self.__replace_custom_chars(lines[i])
                self.lcd.write_string(text)

    def __replace_custom_chars(self, text):
        for search, replace in self.chars.items():
            text = text.replace(search, replace)
        return text

    def create(self, new_char):
        self.lcd.create_char(new_char.code, new_char.bitmap)
        self.chars[new_char.replacement] = chr(new_char.code)

    def close(self):
        self.lcd.close(clear=True)

@contextmanager
def open_lcd():
    lcd = LcdOutput()
    try:
        yield lcd
    finally:
        lcd.close()
