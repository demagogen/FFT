from Fixedpoint import utils

class LUTWithTwiddleFactors:
    def __init__(self):

        # Constants
        self.ADDRESS_GENERATOR_BUS_WIDTH = 10
        self.FFT_BUS_WIDTH               = 32
        self.ROM_BUS_WIDTH               = 32

        # Twiddle factors constants
        self.w40 = utils.Fixedpoint.make_verilog_complex(1, 0)
        self.w41 = utils.Fixedpoint.make_verilog_complex(0, -1)

        # Wire and buses
        self.address_generator = [0] * self.ADDRESS_GENERATOR_BUS_WIDTH
        self.fft               = [0] * self.FFT_BUS_WIDTH
        self.rom               = [0] * self.ROM_BUS_WIDTH

    def twiddle_factors(self):
        return [self.w40, self.w41]
