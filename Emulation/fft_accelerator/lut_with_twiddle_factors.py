import numpy

from fixedpoint import dumps
from fixedpoint.complex_fixedpoint import ComplexFixedpoint

class LUTWithTwiddleFactors:
    def __init__(self):

        # Constants
        self.ADDRESS_GENERATOR_BUS_WIDTH = 10
        self.FFT_BUS_WIDTH = 32
        self.ROM_BUS_WIDTH = 32

        # Twiddle factors constants
        # self.w40 = dumps.Fixedpoint.make_verilog_complex(1, 0)
        # self.w41 = dumps.Fixedpoint.make_verilog_complex(0, -1)

        # Wire and buses
        self.address_generator = [0] * self.ADDRESS_GENERATOR_BUS_WIDTH
        self.fft = [0] * self.FFT_BUS_WIDTH
        self.rom = [0] * self.ROM_BUS_WIDTH

    def twiddle_factor(self, k_root : int, root_power : int) -> ComplexFixedpoint:
        tf = numpy.exp(-2 * numpy.pi * 1j * k_root / root_power)
        tf_cfp = ComplexFixedpoint(tf, 1, 1, 14)
        return tf_cfp

    # def generate_twiddle_factors_from_stage(stage : int) -> list[complex]:


    def twiddle_factors(self, stage : int) -> list[ComplexFixedpoint]:
        tf_fp_list = []
        for index in range(0, stage + 1):
            tf_fp = self.twiddle_factor(index, stage)
            tf_fp_list.append(tf_fp)
        return tf_fp_list
