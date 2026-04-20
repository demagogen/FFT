import numpy


from fft_accelerator.selector import Selector
from fft_accelerator.dual_port_ram import DualPortRAM
from fft_accelerator.fft import FFT4
from fft_accelerator.address_generator import AddressGenerator
from fft_accelerator.control_block import ControlBlock
from fft_accelerator.lut_with_twiddle_factors import LUTWithTwiddleFactors
from fft_accelerator.scale import Scale
from fft_accelerator.rom import ROM
from fft_accelerator.one_depth_buffer import OneDepthBuffer
from fixedpoint.dumps import dumps


from fixedpoint.complex_fixedpoint import ComplexFixedpoint
# from fixedpoint.dumps import Fixedpoint


class FFTAccelerator:
    def __init__(self):

        # Metal Constants
        self.INPUT_DATA_BUS_WIDTH = 16 * 8  # TODO add polymorphism for blocks
        self.OUTPUT_DATA_BUS_WIDTH = 16 * 8  # In every iteration FFT may increase bits
        self.EXCEPTIONS_BUS_WIDTH = 4

        # User constants
        self.COEFFICIENTS_AMOUNT = 4

        # Inputs
        self.input_data = [0] * self.INPUT_DATA_BUS_WIDTH  # Bit reversed!
        self.s_axis_user = 0
        self.s_axis_valid = 0
        self.s_axis_ready = 0
        self.s_axis_last = [0] * self.EXCEPTIONS_BUS_WIDTH

        # Outputs
        self.output_data = [0] * self.OUTPUT_DATA_BUS_WIDTH
        self.m_axis_valid = 0
        self.m_axis_last = 0
        self.m_axis_ready = 0
        self.m_axis_user = 0

        # Blocks
        self.selector = Selector()
        self.dual_port_ram = DualPortRAM()
        # self.fft                      = fft.FFT4()
        self.address_generator = AddressGenerator()
        self.control_block = ControlBlock()
        self.lut_with_twiddle_factors = LUTWithTwiddleFactors()
        self.scale = Scale()
        self.rom = ROM()
        self.one_depth_buffer = OneDepthBuffer()

        # User API
        self.data = [0] * self.COEFFICIENTS_AMOUNT

        # Guts
        self.state = 0

    def data_to_ram(self):
        self.dual_port_ram.ram[0] = self.data[0]
        self.dual_port_ram.ram[1] = self.data[1]
        self.dual_port_ram.ram[2] = self.data[2]
        self.dual_port_ram.ram[3] = self.data[3]

    def fill_user_input(self, input: list[complex]):
        if len(input) != self.COEFFICIENTS_AMOUNT:
            print("Incorrect amount of users coefficients")
        self.data = input

    def take_coeffs(self, addresses : list[int], ram : list[list[int]]) -> list[list[int]]:
        coeff0 = ram[addresses[0]]
        coeff1 = ram[addresses[1]]
        coeff2 = ram[addresses[2]]
        coeff3 = ram[addresses[3]]
        return [coeff0, coeff1, coeff2, coeff3]

    def driver(self, cfp_list : list[ComplexFixedpoint]):
        # print(cfp_bits)
        stage = 1
        self.selector.data_to_ram(
            cfp_list,
            self.dual_port_ram.ram
        )
        addresses = self.address_generator.generate_addresses_for_fft_input()
        # coefficients = self.generate_coefficients_list(addresses)
        coeffs = self.take_coeffs(addresses, self.dual_port_ram.ram)
        twiddle_factors = self.lut_with_twiddle_factors.twiddle_factors(stage)
        my_fft = FFT4()
        fft_result = my_fft.fft_driver(coeffs, twiddle_factors)
        return fft_result


# res = FFTAccelerator()
# result = res.driver([1, 2, 3, 4])
