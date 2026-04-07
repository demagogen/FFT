import utils
import dual_port_ram

class FFT4:
    def __init__(self, polynomial=None):

        # Constants
        self.RAM_INPUT_BUS_WIDTH                = 16 * 8
        self.LUT_WITH_TWIDDLE_FACTORS_BUS_WIDTH = 16 * 2
        self.OUTPUT_BUS_WIDTH                   = 16 * 8
        self.COEFFICIENT_WIDTH                  = 32

        # Wires and busses
        self.ram_input                = [0] * self.RAM_INPUT_BUS_WIDTH
        self.lut_with_twiddle_factors = [0] * self.LUT_WITH_TWIDDLE_FACTORS_BUS_WIDTH
        self.output                   = [0] * self.OUTPUT_BUS_WIDTH

    def __repr__(self):
        return f"FFT4(polynomial='{self.polynomial}', size={self.SIZE})"

    # def split(self):
        # self.partition_polynomial1 = [self.polynomial[0], self.polynomial[2]]
        # self.partition_polynomial2 = [self.polynomial[1], self.polynomial[3]]
#
    # def dft(self):
        # self.partition_vector1[0] = self.partition_polynomial1[0] + self.partition_polynomial1[1] # 0
        # self.partition_vector1[1] = self.partition_polynomial1[0] - self.partition_polynomial1[1] # 2
        # self.partition_vector2[0] = self.partition_polynomial2[0] + self.partition_polynomial2[1] # 1
        # self.partition_vector2[1] = self.partition_polynomial2[0] - self.partition_polynomial2[1] # 3
#
    # def synchronize(self):
        # w40 = complex( 1,  0)
        # w41 = complex( 0,  1)
        # self.result_vector[0] = self.partition_vector1[0] + w40 * self.partition_vector2[0]
        # self.result_vector[3] = self.partition_vector1[1] + w41 * self.partition_vector2[1]
        # self.result_vector[2] = self.partition_vector1[0] - w40 * self.partition_vector2[0]
        # self.result_vector[1] = self.partition_vector1[1] - w41 * self.partition_vector2[1]
        # return self.result_vector

    # def count(self):
        # self.split()
        # self.dft()
        # return self.synchronize()

    def set_coefficients(self, coefficients_from_ram : list) -> list[list[int]]:
        coefficient0 = [0] * self.COEFFICIENT_WIDTH
        coefficient1 = [0] * self.COEFFICIENT_WIDTH
        coefficient2 = [0] * self.COEFFICIENT_WIDTH
        coefficient3 = [0] * self.COEFFICIENT_WIDTH

        print(len(coefficients_from_ram))
        for index in range(0, self.COEFFICIENT_WIDTH):
            coefficient0[index] = coefficients_from_ram[0 * self.COEFFICIENT_WIDTH + index]
            coefficient1[index] = coefficients_from_ram[1 * self.COEFFICIENT_WIDTH + index]
            coefficient2[index] = coefficients_from_ram[2 * self.COEFFICIENT_WIDTH + index]
            coefficient3[index] = coefficients_from_ram[3 * self.COEFFICIENT_WIDTH + index]

        return [coefficient0, coefficient1, coefficient2, coefficient3]

    def fft_driver(self, coefficients_from_ram : list, twiddle_factor1 : list, twiddle_factor2 : list) -> list[complex]:
        # First step
        coefficients = self.set_coefficients(coefficients_from_ram)
        print("Input:")
        utils.Dumps.ram_dump(coefficients_from_ram)
        # utils.Dumps.print_fixedpoint32_list4(utils.Fixedpoint.split_128_to_32(coefficients_from_ram))
        utils.Dumps.print_nested_bits_as_complex(utils.Fixedpoint.split_128_to_32(coefficients_from_ram))

        partition_coefficients1 = [[0] * self.COEFFICIENT_WIDTH] * 2
        partition_coefficients2 = [[0] * self.COEFFICIENT_WIDTH] * 2
        print("Partitions init")
        utils.Dumps.print_fixedpoint32_listn(partition_coefficients1, 2)
        utils.Dumps.print_fixedpoint32_listn(partition_coefficients2, 2)
        partition_coefficients1[0] = utils.Fixedpoint.add_bits_32(coefficients[0], coefficients[1])
        partition_coefficients1[1] = utils.Fixedpoint.sub_bits_32(coefficients[0], coefficients[1])
        partition_coefficients2[0] = utils.Fixedpoint.add_bits_32(coefficients[0], coefficients[1])
        partition_coefficients2[1] = utils.Fixedpoint.sub_bits_32(coefficients[0], coefficients[1])
        print("First step")
        utils.Dumps.print_fixedpoint32_listn(partition_coefficients1, 2)
        utils.Dumps.print_fixedpoint32_listn(partition_coefficients2, 2)
        print(utils.Fixedpoint.bits_to_complex(partition_coefficients1[0]))
        print(utils.Fixedpoint.bits_to_complex(partition_coefficients1[1]))
        print(utils.Fixedpoint.bits_to_complex(partition_coefficients2[0]))
        print(utils.Fixedpoint.bits_to_complex(partition_coefficients2[1]))
        result_coefficients = [[0] * self.COEFFICIENT_WIDTH] * 4
        print("Result init")
        utils.Dumps.print_fixedpoint32_list4(result_coefficients)
        result_coefficients[0] = utils.Fixedpoint.add_bits_32(partition_coefficients1[0], utils.Fixedpoint.mult_bits_32(partition_coefficients2[0], twiddle_factor1))
        result_coefficients[1] = utils.Fixedpoint.sub_bits_32(partition_coefficients1[0], utils.Fixedpoint.mult_bits_32(partition_coefficients2[0], twiddle_factor1))
        result_coefficients[2] = utils.Fixedpoint.add_bits_32(partition_coefficients1[1], utils.Fixedpoint.mult_bits_32(partition_coefficients2[1], twiddle_factor2))
        result_coefficients[3] = utils.Fixedpoint.sub_bits_32(partition_coefficients1[1], utils.Fixedpoint.mult_bits_32(partition_coefficients2[1], twiddle_factor2))
        print("result")
        utils.Dumps.print_fixedpoint32_list4(result_coefficients)
        # utils.Dumps.print_nested_bits_as_complex(result_coefficients)
        return result_coefficients




