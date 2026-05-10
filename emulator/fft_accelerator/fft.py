import numpy
import math
from fixedpoint.fixedpoint import Fixedpoint
from fixedpoint.complex_fixedpoint import ComplexFixedpoint
from fft_accelerator.lut_with_twiddle_factors import LUTWithTwiddleFactors

PARAMS = {
    "with_sign": 1,
    "frac_width": 14,
    "width": 16,
    "saturate": True,
    "rounding": False,
}


class FFT:
    def __repr__(self):
        return f"FFT(polynomial='{self .polynomial }', size={self .SIZE })"

    def radix2(
        self, coeffs: list[ComplexFixedpoint], twiddle_factors
    ) -> list[ComplexFixedpoint]:
        x0, x1 = coeffs
        result1 = x0 + x1
        result2 = x0 - x1
        return [result1, result2]

    def radix4(self, coeffs):
        x0, x1, x2, x3 = coeffs

        t0 = x0 + x2
        t1 = x1 + x3
        t2 = x0 - x2
        t3 = x1 - x3

        minus_j = ComplexFixedpoint(complex(0, -1), **PARAMS)

        y0 = t0 + t1
        y1 = t2 + minus_j * t3
        y2 = t0 - t1
        y3 = t2 - minus_j * t3

        return [y0, y1, y2, y3]

    def radix8(
        self, coeffs: list[ComplexFixedpoint], twiddle_factors=None
    ) -> list[ComplexFixedpoint]:
        x0, x1, x2, x3, x4, x5, x6, x7 = coeffs
        tmp0, tmp1, tmp2, tmp3 = self.radix4([x0, x2, x4, x6])
        tmp4, tmp5, tmp6, tmp7 = self.radix4([x1, x3, x5, x7])
        lut = LUTWithTwiddleFactors()
        w08 = lut.twiddle_factor(0, 8)
        w18 = lut.twiddle_factor(1, 8)
        w28 = lut.twiddle_factor(2, 8)
        w38 = lut.twiddle_factor(3, 8)
        result0 = tmp0 + w08 * tmp4
        result4 = tmp0 - w08 * tmp4
        result1 = tmp1 + w18 * tmp5
        result5 = tmp1 - w18 * tmp5
        result2 = tmp2 + w28 * tmp6
        result6 = tmp2 - w28 * tmp6
        result3 = tmp3 + w38 * tmp7
        result7 = tmp3 - w38 * tmp7
        return [result0, result1, result2, result3, result4, result5, result6, result7]

    def radix16(
        self, coeffs: list[ComplexFixedpoint], twiddle_factors=None
    ) -> list[ComplexFixedpoint]:
        addresses, weights = FFT.gen_addr(int(math.log2(len(coeffs))))
        print("Addresses: ", addresses)
        print("Weights: ", weights)
        #         for i in range(len(addresses)):
        #             addr = addresses[i]
        #             w    = weights[i]
        #
        #             input = [
        #                 coeffs[addr[0]],
        #                 coeffs[addr[1]],
        #                 coeffs[addr[2]],
        #                 coeffs[addr[3]],
        #             ]
        #             tmp = self.radix4(input)
        #
        #
        #             coeffs[addr[0]] = tmp[0]
        #             coeffs[addr[1]] = tmp[1] * w[1]
        #             coeffs[addr[2]] = tmp[2] * w[2]
        #             coeffs[addr[3]] = tmp[3] * w[3]
        for stage in range(len(addresses)):
            # for addr in range(len(addresses[stage])):
            addr = addresses[stage]
            w = weights[stage]
            input = [coeffs[addr[0]], coeffs[addr[1]], coeffs[addr[2]], coeffs[addr[3]]]
            tmp = self.radix4(input)
            coeffs[addr[0]] = tmp[0]
            coeffs[addr[1]] = tmp[1] * w[1]
            coeffs[addr[2]] = tmp[2] * w[2]
            coeffs[addr[3]] = tmp[3] * w[3]

        return coeffs
