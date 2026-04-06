class ROM:
    def __init__(self):

        # Constants
        self.LUT_WITH_TWIDDLE_FACTORS_BUS_WIDTH = 32

        # Wires and buses
        self.lut_with_twiddle_factors = [0] * self.LUT_WITH_TWIDDLE_FACTORS_BUS_WIDTH


