from fixedpoint.validator import validate

import numpy

class Fixedpoint:
    @classmethod
    @validate
    def __init__(self, value : float, with_sign : int, frac_width : int, width : int):
        self.nested_bits = [0]
        self.raw_value = 0
        self.width = width
        self.frac_width = frac_width
        self.with_sign = with_sign

        self.raw_value = int(numpy.round(value * 2 ** frac_width))
        mask = (1 << width) - 1
        unsigned_raw = self.raw_value & mask
        self.nested_bits = [(unsigned_raw >> i) & 1 for i in range(width - 1, -1, -1)]

