from time import sleep

class SerialDisplay(object):
    def __init__(self, display, delay):
        self.display = display
        self.delay = delay

    def update(self, *lines):
        self.display.update(*lines)
        sleep(self.delay)
