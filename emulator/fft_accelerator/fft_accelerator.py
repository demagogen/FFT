import numpy
from fft_accelerator.fft import FFT
from fft_accelerator.address_generator import AddressGenerator
from fft_accelerator.lut_with_twiddle_factors import LUTWithTwiddleFactors
from fixedpoint.complex_fixedpoint import ComplexFixedpoint


class FFTAccelerator:
    def __init__(self):
        self.INPUT_DATA_BUS_WIDTH = 16 * 8
        self.OUTPUT_DATA_BUS_WIDTH = 16 * 8
        self.EXCEPTIONS_BUS_WIDTH = 4
        self.COEFFICIENTS_AMOUNT = 4
        self.input_data = [0] * self.INPUT_DATA_BUS_WIDTH
        self.s_axis_user = 0
        self.s_axis_valid = 0
        self.s_axis_ready = 0
        self.s_axis_last = [0] * self.EXCEPTIONS_BUS_WIDTH
        self.output_data = [0] * self.OUTPUT_DATA_BUS_WIDTH
        self.m_axis_valid = 0
        self.m_axis_last = 0
        self.m_axis_ready = 0
        self.m_axis_user = 0
        self.address_generator = AddressGenerator()
        self.lut_with_twiddle_factors = LUTWithTwiddleFactors()
        self.data = [0] * self.COEFFICIENTS_AMOUNT
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

    def take_coeffs(
        self, addresses: list[int], ram: list[list[int]]
    ) -> list[list[int]]:
        coeff0 = ram[addresses[0]]
        coeff1 = ram[addresses[1]]
        coeff2 = ram[addresses[2]]
        coeff3 = ram[addresses[3]]
        return [coeff0, coeff1, coeff2, coeff3]

    def driver(self, cfp_list: list[ComplexFixedpoint]):
        stage = 1
        my_fft = FFT()
        fft_result = my_fft.radix4(cfp_list)
        return fft_result
