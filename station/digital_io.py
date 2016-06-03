from time import sleep
import RPi.GPIO as GPIO

class DigitalIO(object):
    def __init__(self, pin):
        self.pin = pin

    def setup_in(self):
        GPIO.setup(self.pin, GPIO.IN)

    def setup_out(self):
        GPIO.setup(self.pin, GPIO.OUT)

    def read(self):
        return GPIO.input(self.pin)

    def write(self, value):
        GPIO.output(self.pin, GPIO.HIGH if value else GPIO.LOW)

    def wait_for_edge(self):
        GPIO.wait_for_edge(self.pin, GPIO.BOTH)

    def wait_for_rising(self):
        GPIO.wait_for_edge(self.pin, GPIO.RISING)

    def wait_for_falling(self):
        GPIO.wait_for_edge(self.pin, GPIO.FALLING)

    @staticmethod
    def usleep(microseconds):
        sleep(microseconds * 1E-6)

    @staticmethod
    def msleep(milliseconds):
        sleep(milliseconds * 1E-3)
