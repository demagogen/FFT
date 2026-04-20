from fixedpoint.dumps import dumps
from fixedpoint.dumps import Fixedpoint
from fft_accelerator.dual_port_ram import DualPortRAM
from fixedpoint.complex_fixedpoint import ComplexFixedpoint


class FFT4:
    def __init__(self, polynomial=None):

        # Constants
        self.RAM_INPUT_BUS_WIDTH = 16 * 8
        self.LUT_WITH_TWIDDLE_FACTORS_BUS_WIDTH = 16 * 2
        self.OUTPUT_BUS_WIDTH = 16 * 8
        self.COEFFICIENT_WIDTH = 32

        # Wires and busses
        self.ram_input = [0] * self.RAM_INPUT_BUS_WIDTH
        self.lut_with_twiddle_factors = [0] * self.LUT_WITH_TWIDDLE_FACTORS_BUS_WIDTH
        self.output = [0] * self.OUTPUT_BUS_WIDTH

    def __repr__(self):
        return f"FFT4(polynomial='{self.polynomial}', size={self.SIZE})"

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
        self, coeffs: list[ComplexFixedpoint], twiddle_factors : list[ComplexFixedpoint]
    ) -> list[ComplexFixedpoint]:
        # coefficients = self.set_coefficients(coefficients_from_ram)
        # dumps.print_fixedpoint32_list4(coefficients)
        # partition_coefficients1 = [[0] * self.COEFFICIENT_WIDTH] * 2
        # partition_coefficients2 = [[0] * self.COEFFICIENT_WIDTH] * 2
        # partition_coefficients1[0] = Fixedpoint.add_bits_32(
            # coefficients[0], coefficients[1]
        # )
        # partition_coefficients1[1] = Fixedpoint.sub_bits_32(
            # coefficients[0], coefficients[1]
        # )
        # partition_coefficients2[0] = Fixedpoint.add_bits_32(
            # coefficients[2], coefficients[3]
        # )
        # partition_coefficients2[1] = Fixedpoint.sub_bits_32(
            # coefficients[2], coefficients[3]
        # )

        # print("partition coefficients")
        # dumps.print_fixedpoint32(partition_coefficients1[0])
        # dumps.print_fixedpoint32(partition_coefficients1[1])
        # dumps.print_fixedpoint32(partition_coefficients2[0])
        # dumps.print_fixedpoint32(partition_coefficients2[1])
        # print("as complex")
        # dumps.print_as_complex(partition_coefficients1[0])
        # dumps.print_as_complex(partition_coefficients1[1])
        # dumps.print_as_complex(partition_coefficients2[0])
        # dumps.print_as_complex(partition_coefficients2[1])

        coeff00 = coeffs[0]
        coeff01 = coeffs[1]
        coeff10 = coeffs[2]
        coeff11 = coeffs[3]

        # tmp_cfp00 = coeff0 + twiddle_factor1

<<<<<<< HEAD
        tmp_cfp00 = coeff00 + twiddle_factors[0] * coeff01
        tmp_cfp01 = coeff00 - twiddle_factors[1] * coeff01
        tmp_cfp10 = coeff01 + twiddle_factors[0] * coeff11
        tmp_cfp11 = coeff01 - twiddle_factors[1] * coeff11

        result_cfp0 = tmp_cfp00 + twiddle_factors[2] * tmp_cfp10
        result_cfp1 = tmp_cfp00 - twiddle_factors[2] * tmp_cfp10
        result_cfp2 = tmp_cfp01 + twiddle_factors[3] * tmp_cfp11
        result_cfp3 = tmp_cfp01 - twiddle_factors[3] * tmp_cfp11
=======

<<<<<<< HEAD
        result_cfp0 = coeff00 + twiddle_factors[0] * coeff10
        result_cfp1 = coeff00 - twiddle_factors[0] * coeff10
        result_cfp2 = coeff01 + twiddle_factors[1] * coeff11
        result_cfp3 = coeff01 - twiddle_factors[1] * coeff11
>>>>>>> parent of d9e5907 (add tests and changed fft)
=======
        tmp_cfp00 = coeff00 + twiddle_factors[0] * coeff01
        tmp_cfp01 = coeff00 - twiddle_factors[1] * coeff01
        tmp_cfp10 = coeff01 + twiddle_factors[0] * coeff11
        tmp_cfp11 = coeff01 - twiddle_factors[1] * coeff11

        result_cfp0 = tmp_cfp00 + twiddle_factors[2] * tmp_cfp10
        result_cfp1 = tmp_cfp00 - twiddle_factors[2] * tmp_cfp10
        result_cfp2 = tmp_cfp01 + twiddle_factors[3] * tmp_cfp11
        result_cfp3 = tmp_cfp01 - twiddle_factors[3] * tmp_cfp11
>>>>>>> d9e59079d9e00bf24800610857b94475a01dcc7b

        # result_coefficients = [[0] * self.COEFFICIENT_WIDTH] * 4
        # result_coefficients[0] = Fixedpoint.add_bits_32(
            # partition_coefficients1[0],
            # Fixedpoint.mult_bits_32(partition_coefficients2[0], twiddle_factor1),
        # )
        # result_coefficients[1] = Fixedpoint.add_bits_32(
            # partition_coefficients1[1],
            # Fixedpoint.mult_bits_32(partition_coefficients2[1], twiddle_factor2),
        # )
        # result_coefficients[2] = Fixedpoint.sub_bits_32(
            # partition_coefficients1[0],
            # Fixedpoint.mult_bits_32(partition_coefficients2[0], twiddle_factor1),
        # )
        # result_coefficients[3] = Fixedpoint.sub_bits_32(
            # partition_coefficients1[1],
            # Fixedpoint.mult_bits_32(partition_coefficients2[1], twiddle_factor2),
        # )

        # print("result")
        # dumps.print_fixedpoint32_list4(result_coefficients)
        # dumps.print_as_complex(result_coefficients[0])
        # dumps.print_as_complex(result_coefficients[1])
        # dumps.print_as_complex(result_coefficients[2])
        # dumps.print_as_complex(result_coefficients[3])

        # print("Twiddle factors")
        # print(twiddle_factor1)
        # print(twiddle_factor2)

        # print("end fft_driver")
        return [result_cfp0, result_cfp1, result_cfp2, result_cfp3]
