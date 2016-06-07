from station.measurement import Measurement
from station.spi_sensor import SpiSensor

class GasSensor(SpiSensor):
    def __init__(self, device, circuit):
        super().__init__(device)
        self.circuit = circuit

    def read(self):
        voltage = self.device.voltage()
        resistance = self.circuit.get_resistance(voltage)
        return (
            Measurement(name='air contaminants', abbrev='air', value=resistance, units='Ω'),
        )
