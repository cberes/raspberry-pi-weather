from contextlib import contextmanager
import RPi.GPIO as GPIO
from RPLCD import CharLCD, cleared

class LcdOutput(object):
    def __init__(self):
        self.lcd = CharLCD(pin_rs=3, pin_e=5, pins_data=[18, 22, 7, 13],
                           pin_rw=None, numbering_mode=GPIO.BOARD,
                           cols=16, rows=2, dotsize=8)

    def update(self, *lines):
        with cleared(self.lcd):
            for i in range(0, len(lines)):
                self.lcd.cursor_pos = (i, 0)
                self.lcd.write_string(lines[i])

    def create(self, new_char):
        self.lcd.create_char(new_char.code, new_char.bitmap)

    def close(self):
        self.lcd.close(clear=True)

@contextmanager
def open_lcd():
    lcd = LcdOutput()
    try:
        yield lcd
    finally:
        lcd.close()
