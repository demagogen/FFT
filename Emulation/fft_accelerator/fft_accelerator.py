from fft_accelerator.selector import Selector
from fft_accelerator.dual_port_ram import DualPortRAM
# from fft_accelerator.fft import FFT4
from fft_accelerator.address_generator import AddressGenerator
from fft_accelerator.control_block import ControlBlock
from fft_accelerator.lut_with_twiddle_factors import LUTWithTwiddleFactors
from fft_accelerator.scale import Scale
from fft_accelerator.rom import ROM
from fft_accelerator.one_depth_buffer import OneDepthBuffer
import numpy
from fixedpoint.dumps import dumps
# from fixedpoint.dumps import Fixedpoint

class FFTAccelerator:
    def __init__(self):

        # Metal Constants
        self.INPUT_DATA_BUS_WIDTH  = 16 * 8 #TODO add polymorphism for blocks
        self.OUTPUT_DATA_BUS_WIDTH = 16 * 8 #In every iteration FFT may increase bits
        self.EXCEPTIONS_BUS_WIDTH  = 4

        # User constants
        self.COEFFICIENTS_AMOUNT = 4

        # Inputs
        self.input_data   = [0] * self.INPUT_DATA_BUS_WIDTH #Bit reversed!
        self.s_axis_user  = 0
        self.s_axis_valid = 0
        self.s_axis_ready = 0
        self.s_axis_last  = [0] * self.EXCEPTIONS_BUS_WIDTH

        # Outputs
        self.output_data  = [0] * self.OUTPUT_DATA_BUS_WIDTH
        self.m_axis_valid = 0
        self.m_axis_last  = 0
        self.m_axis_ready = 0
        self.m_axis_user  = 0

        # Blocks
        self.selector                 = Selector()
        self.dual_port_ram            = DualPortRAM()
        # self.fft                      = fft.FFT4()
        self.address_generator        = AddressGenerator()
        self.control_block            = ControlBlock()
        self.lut_with_twiddle_factors = LUTWithTwiddleFactors()
        self.scale                    = Scale()
        self.rom                      = ROM()
        self.one_depth_buffer         = OneDepthBuffer()

        # User API
        self.data = [0] * self.COEFFICIENTS_AMOUNT

        # Guts
        self.state = 0

    def data_to_ram(self):
        self.dual_port_ram.ram[0] = self.data[0]
        self.dual_port_ram.ram[1] = self.data[1]
        self.dual_port_ram.ram[2] = self.data[2]
        self.dual_port_ram.ram[3] = self.data[3]

    def fill_user_input(self, input : list[complex]):
        if len(input) != self.COEFFICIENTS_AMOUNT:
            print("Incorrect amount of users coefficients")
        self.data = input

    def generate_coefficients_list(self, input_addresses : list[int]):
        coefficient0 = [0] * 32
        coefficient1 = [0] * 32
        coefficient2 = [0] * 32
        coefficient3 = [0] * 32
        for index in range(0, 32):
            coefficient0[index] = self.dual_port_ram.ram[input_addresses[0] * 32 + index]
            coefficient1[index] = self.dual_port_ram.ram[input_addresses[1] * 32 + index]
            coefficient2[index] = self.dual_port_ram.ram[input_addresses[2] * 32 + index]
            coefficient3[index] = self.dual_port_ram.ram[input_addresses[3] * 32 + index]
        return coefficient0 + coefficient1 + coefficient2 + coefficient3
        # return [self.dual_port_ram.ram[input_addresses[0]], self.dual_port_ram.ram[input_addresses[1]], self.dual_port_ram.ram[input_addresses[2]], self.dual_port_ram.ram[input_addresses[3]]]

    def driver(self, data_fixedpoint : list[complex]):
        # data_fixedpoint = dumps.Fixedpoint.complex_to_verilog_bits(user_input)
        self.selector.fill_input_data(data_fixedpoint, self.dual_port_ram.ram, self.address_generator.generate_input_addresses(self.state))
        addresses = self.address_generator.generate_addresses_for_fft_input()
        coefficients = self.generate_coefficients_list(addresses)
        # dumps.dumps.print_fixedpoint32_nested_bytes_list4(coefficients)
        twiddle_factor1 = self.lut_with_twiddle_factors.twiddle_factors()[0]
        twiddle_factor2 = self.lut_with_twiddle_factors.twiddle_factors()[1]
        my_fft = FFT.FFT4()
        fft_result = my_fft.fft_driver(coefficients, twiddle_factor1, twiddle_factor2)
        return fft_result

# def fft_accelerator_int_test():
#     fft = FFTAccelerator()
#     for coeff0 in range(0, 10):
#         for coeff1 in range(0, 10):
#             for coeff2 in range(0, 10):
#                 for coeff3 in range(0, 10):
#                     fixedpoint_coeffs = dumps.Fixedpoint.complex_to_verilog_bits([coeff0, coeff1, coeff2, coeff3])
#                     print("fft_accelerator fp")
#                     dumps.dumps.print_fixedpoint32_nested_bytes_list4(fixedpoint_coeffs)
#                     fft_result = fft.driver(fixedpoint_coeffs)
#                     fft_result_python_complex = dumps.Fixedpoint.nested_bits_to_complex(fft_result)
#                     expected = numpy.fft.fft([coeff0, coeff1, coeff2, coeff3])
#                     if numpy.allclose(fft_result_python_complex, expected, atol=0.1):
#                         print("True:  ", [coeff0, coeff1, coeff2, coeff3], ", numpy: " , expected, ", fft: ", fft_result_python_complex,)
#                     else:
#                         print("False: ", [coeff0, coeff1, coeff2, coeff3], ", numpy: ", expected, ", fft: ", fft_result_python_complex)
#                         return
#
# def fft_accelerator_float_test():
#     fft = FFTAccelerator()
#     for coeff0 in numpy.arange(0.0, 1.1, 0.1):
#         for coeff1 in numpy.arange(0.0, 1.1, 0.1):
#             for coeff2 in numpy.arange(0.0, 1.1, 0.1):
#                 for coeff3 in numpy.arange(0.0, 1.1, 0.1):
#                     fixedpoint_coeffs = dumps.Fixedpoint.complex_to_verilog_bits([coeff0, coeff1, coeff2, coeff3])
#                     fft_result = fft.driver(fixedpoint_coeffs)
#                     fft_result_python_complex = dumps.Fixedpoint.nested_bits_to_complex(fft_result)
#                     expected = numpy.fft.fft([coeff0, coeff1, coeff2, coeff3])
#                     if numpy.allclose(fft_result_python_complex, expected, atol=0.1):
#                         print("True: ", [coeff0, coeff1, coeff2, coeff3], ", numpy: " , expected, ", fft: ", fft_result_python_complex,)
#                     else:
#                         print("False: ", [coeff0, coeff1, coeff2, coeff3], ", numpy: ", expected, ", fft: ", fft_result_python_complex)
#                         return

def main():
    fft_accelerator = FFTAccelerator()
    fft_accelerator_result = fft_accelerator.driver([1, -1, 1, -1])
    coeffs = dumps.Fixedpoint.nested_bits_to_complex(fft_accelerator_result)
    for coeff in range(0, 4):
        print("#", coeff, ": ", coeffs[coeff])
    for string in range(0, 4):
        print("#", string, ": ", end="")
        for column in range(0, 32):
            print(fft_accelerator_result[string][column], end="")
        print()

# main()
# fft_accelerator_int_test()
# fft_accelerator_float_test()
