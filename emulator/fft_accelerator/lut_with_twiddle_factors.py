import numpy
import math
from fixedpoint.complex_fixedpoint import ComplexFixedpoint

PARAMS = {
    "with_sign": 1,
    "frac_width": 14,
    "width": 16,
    "saturate": True,
    "rounding": False,
}


class LUTWithTwiddleFactors:
    def twiddle_factor(self, k_root: int, root_power: int) -> ComplexFixedpoint:
        if root_power <= 0:
            root_power = 4
        tf = numpy.exp(-2 * numpy.pi * 1j * k_root / root_power)
        return ComplexFixedpoint(tf, **PARAMS)

    def generate_twiddles(self, amount):
        radix = 4
        stages = int(math.log(amount, radix))
        twiddles = []
        for stage in range(0, stages):
            stride = radix**stage
            group = radix * stride
            stage_twiddles = []
            for base in range(0, amount, group):
                for offset in range(0, stride):
                    k = offset * (amount // group)
                    stage_twiddles.append(
                        [
                            self.twiddle_factor(0 * k, amount),
                            self.twiddle_factor(1 * k, amount),
                            self.twiddle_factor(2 * k, amount),
                            self.twiddle_factor(3 * k, amount),
                        ]
                    )
            twiddles.append(stage_twiddles)
        return twiddles
