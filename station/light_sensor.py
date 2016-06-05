from station.gas_sensor import GasSensor

class LightSensor(GasSensor):
    def __init__(self, read_channel, circuit):
        super().__init__(read_channel, circuit)

    def read(self):
        # apparently light resistance (in KΩ) = 500 / Lux
        return 500000 / super().read()
