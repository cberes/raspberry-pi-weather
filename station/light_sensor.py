from station.gas_sensor import GasSensor
from station.measurement import Measurement

class LightSensor(GasSensor):
    def __init__(self, device, circuit):
        super().__init__(device, circuit)

    def read(self):
        # apparently light resistance (in KΩ) = 500 / Lux
        resistance = super().read()[0].get_value()
        lux = 0 if resistance == 0 else 500000 / resistance
        return (
            Measurement(name='light', abbrev='lit', value=lux, units='lx'),
        )
