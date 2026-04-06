import selector
import dual_port_ram
import fft
import address_generator
import control_block
import lut_with_twiddle_factors
import scale
import rom
import one_depth_buffer
import utils

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
        self.selector                 = selector.Selector()
        self.dual_port_ram            = dual_port_ram.DualPortRAM()
        # self.fft                      = fft.FFT4()
        self.address_generator        = address_generator.AddressGenerator()
        self.control_block            = control_block.ControlBlock()
        self.lut_with_twiddle_factors = lut_with_twiddle_factors.LUTWithTwiddleFactors()
        self.scale                    = scale.Scale()
        self.rom                      = rom.ROM()
        self.one_depth_buffer         = one_depth_buffer.OneDepthBuffer()

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
            coefficient0[index] = self.dual_port_ram.ram[0 * 32 + index]
            coefficient1[index] = self.dual_port_ram.ram[1 * 32 + index]
            coefficient2[index] = self.dual_port_ram.ram[2 * 32 + index]
            coefficient3[index] = self.dual_port_ram.ram[3 * 32 + index]
        return coefficient0 + coefficient1 + coefficient2 + coefficient3
        # return [self.dual_port_ram.ram[input_addresses[0]], self.dual_port_ram.ram[input_addresses[1]], self.dual_port_ram.ram[input_addresses[2]], self.dual_port_ram.ram[input_addresses[3]]]

    def driver(self, user_input : list[complex]):
        data_fixedpoint = utils.Fixedpoint.complex_to_verilog_bits(user_input)
        self.selector.fill_input_data(data_fixedpoint, self.dual_port_ram.ram, self.address_generator.generate_input_addresses(self.state))
        self.dual_port_ram.dump()
        addresses = self.address_generator.generate_addresses_for_fft_input(0)
        coefficients = self.generate_coefficients_list(addresses)
        for i in range(0, len(coefficients)):
            print(coefficients[0])
        # coefficients_arr = coefficients[0] + coefficients[1] + coefficients[2] + coefficients[3]
        twiddle_factor1 = self.lut_with_twiddle_factors.twiddle_factors()[0]
        twiddle_factor2 = self.lut_with_twiddle_factors.twiddle_factors()[1]
        my_fft = fft.FFT4()
        fft_result = my_fft.fft_driver(coefficients, twiddle_factor1, twiddle_factor2)
        return fft_result


def main():
    fft_accelerator = FFTAccelerator()
    fft_accelerator_result = fft_accelerator.driver([1, 2, 3, 4])
    # print(fft_accelerator_result)

main()
