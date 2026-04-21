import numpy

from fixedpoint.complex_fixedpoint import ComplexFixedpoint

PARAMS = {
    "with_sign": 1,
    "frac_width": 14,
    "width": 16,
    "saturate": True,
    "rounding": False,
}


class LUTWithTwiddleFactors:
    def __init__(self):

        self.ADDRESS_GENERATOR_BUS_WIDTH = 10
        self.FFT_BUS_WIDTH = 32
        self.ROM_BUS_WIDTH = 32

        self.address_generator = [0] * self.ADDRESS_GENERATOR_BUS_WIDTH
        self.fft = [0] * self.FFT_BUS_WIDTH
        self.rom = [0] * self.ROM_BUS_WIDTH

    def twiddle_factor(self, k_root: int, root_power: int) -> ComplexFixedpoint:

        if root_power <= 0:
            root_power = 4
        tf = numpy.exp(-2 * numpy.pi * 1j * k_root / root_power)

        return ComplexFixedpoint(tf, **PARAMS)

    def twiddle_factors(self, stage: int) -> list[ComplexFixedpoint]:
        tf_fp_list = []

        for index in range(0, (stage * 4)):
            tf_fp_extra = self.twiddle_factor(index, stage)
            tf_fp_list.append(tf_fp_extra)

        return tf_fp_list
