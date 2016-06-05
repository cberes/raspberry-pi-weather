class VoltageDivider(object):
    def __init__(self, v_dc, r_load1, r_load2):
        self.v_dc = v_dc
        self.r_load1 = r_load1
        self.r_load2 = r_load2

    def get_resistance(self, v_out):
        return 0 if v_out == 0 else (self.v_dc / v_out * self.r_load2 - self.r_load1 - self.r_load2)
