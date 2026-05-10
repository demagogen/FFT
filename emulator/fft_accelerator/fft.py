import math

import numpy

from fft_accelerator.address_generator import AddressGenerator
from fft_accelerator.lut_with_twiddle_factors import LUTWithTwiddleFactors
from fixedpoint.complex_fixedpoint import ComplexFixedpoint
from fixedpoint.fixedpoint import Fixedpoint

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
        minus_j = ComplexFixedpoint(complex(0, -1), **PARAMS)
        a = x0 + x2
        b = x0 - x2
        c = x1 + x3
        d = (x1 - x3) * minus_j
        y0 = a + c
        y1 = b + d
        y2 = a - c
        y3 = b - d
        return [y0, y1, y2, y3]

    def radix8(
        self, coeffs: list[ComplexFixedpoint], twiddle_factors=None
    ) -> list[ComplexFixedpoint]:
        x0, x1, x2, x3, x4, x5, x6, x7 = coeffs
        tmp0, tmp1, tmp2, tmp3 = self.radix4([x0, x2, x4, x6])
        tmp4, tmp5, tmp6, tmp7 = self.radix4([x1, x3, x5, x7])
        w08 = LUTWithTwiddleFactors.twiddle_factor(0, 8)
        w18 = LUTWithTwiddleFactors.twiddle_factor(1, 8)
        w28 = LUTWithTwiddleFactors.twiddle_factor(2, 8)
        w38 = LUTWithTwiddleFactors.twiddle_factor(3, 8)
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
        addresses = AddressGenerator.generate_addresses(int(math.log2(len(coeffs))))
        twiddles = LUTWithTwiddleFactors.generate_twiddles(int(math.log2(len(coeffs))))

    def driver_radix4(self, coeffs):
        amount = len(coeffs)
        addresses = AddressGenerator.generate_addresses(amount)
        twiddles = LUTWithTwiddleFactors.generate_twiddles(amount)
        stages = len(addresses)
        for stage in range(0, stages):
            for butterfly_index in range(0, len(addresses[stage])):
                address = addresses[stage][butterfly_index]
                input_twiddles = twiddles[stage][butterfly_index]
                scale = ComplexFixedpoint(0.25, **PARAMS)

                input_coeffs = [
                    coeffs[address[0]] * scale,
                    coeffs[address[1]] * input_twiddles[1] * scale,
                    coeffs[address[2]] * input_twiddles[2] * scale,
                    coeffs[address[3]] * input_twiddles[3] * scale,
                ]
                result = self.radix4(input_coeffs)
                scale = ComplexFixedpoint(0.25, **PARAMS)
                coeffs[address[0]] = result[0]
                coeffs[address[1]] = result[1]
                coeffs[address[2]] = result[2]
                coeffs[address[3]] = result[3]
        return coeffs

    def digit_reverse_base4(self, index, digits):
        result = 0
        for digit in range(digits):
            result = result * 4 + (index % 4)
            index //= 4
        return result

    def reorder_radix4(self, data):
        amount = len(data)
        digits = int(math.log(amount, 4))
        reordered = [0] * amount
        for index in range(amount):
            new_index = self.digit_reverse_base4(index, digits)
            reordered[index] = data[new_index]
        return reordered
