class VoltageLoad(object):
    def __init__(self, v_dc, r_load):
        self.v_dc = v_dc
        self.r_load = r_load

    def get_resistance(self, v_out):
        return 0 if v_out == 0 else (self.v_dc / v_out * self.r_load - self.r_load)
