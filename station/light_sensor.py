from station.gas_sensor import GasSensor

class LightSensor(GasSensor):
    def __init__(self, read_channel, circuit):
        super().__init__(read_channel, circuit)

    def read(self):
        # apparently light resistance (in KΩ) = 500 / Lux
        resistance = super().read()
        return 0 if resistance == 0 else 500000 / resistance
