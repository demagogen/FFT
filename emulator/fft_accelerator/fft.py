from fixedpoint.fixedpoint import Fixedpoint
from fft_accelerator.dual_port_ram import DualPortRAM
from fixedpoint.complex_fixedpoint import ComplexFixedpoint

PARAMS = {
    "with_sign": 1,
    "frac_width": 14,
    "width": 16,
    "saturate": True,
    "rounding": False,
}


class FFT4:
    def __init__(self, polynomial=None):

        self.RAM_INPUT_BUS_WIDTH = 16 * 8
        self.LUT_WITH_TWIDDLE_FACTORS_BUS_WIDTH = 16 * 2
        self.OUTPUT_BUS_WIDTH = 16 * 8
        self.COEFFICIENT_WIDTH = 32

        self.ram_input = [0] * self.RAM_INPUT_BUS_WIDTH
        self.lut_with_twiddle_factors = [0] * self.LUT_WITH_TWIDDLE_FACTORS_BUS_WIDTH
        self.output = [0] * self.OUTPUT_BUS_WIDTH

    def __repr__(self):
        return f"FFT4(polynomial='{self .polynomial }', size={self .SIZE })"

    def set_coefficients(self, coefficients_from_ram: list[ComplexFixedpoint]):
        coefficient0 = [0] * self.COEFFICIENT_WIDTH
        coefficient1 = [0] * self.COEFFICIENT_WIDTH
        coefficient2 = [0] * self.COEFFICIENT_WIDTH
        coefficient3 = [0] * self.COEFFICIENT_WIDTH

        for index in range(0, self.COEFFICIENT_WIDTH):
            coefficient0[index] = coefficients_from_ram[
                0 * self.COEFFICIENT_WIDTH + index
            ]
            coefficient1[index] = coefficients_from_ram[
                1 * self.COEFFICIENT_WIDTH + index
            ]
            coefficient2[index] = coefficients_from_ram[
                2 * self.COEFFICIENT_WIDTH + index
            ]
            coefficient3[index] = coefficients_from_ram[
                3 * self.COEFFICIENT_WIDTH + index
            ]

        return [coefficient0, coefficient1, coefficient2, coefficient3]

    def fft_driver(
        self, coeffs: list[ComplexFixedpoint], twiddle_factors
    ) -> list[ComplexFixedpoint]:
        x0, x1, x2, x3 = coeffs

        tmp1 = x0 + x2
        tmp2 = x0 - x2
        tmp3 = x1 + x3
        tmp4 = x1 - x3

        minus_j = ComplexFixedpoint(complex(0, -1), **PARAMS)

        result1 = tmp1 + tmp3
        result2 = tmp1 - tmp3

        j_term = minus_j * tmp4

        r1 = tmp2 + j_term
        r3 = tmp2 - j_term

        return [result1, r1, result2, r3]
