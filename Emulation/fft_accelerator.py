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
        return [self.dual_port_ram.ram[input_addresses[0]], self.dual_port_ram.ram[input_addresses[1]], self.dual_port_ram.ram[input_addresses[2]], self.dual_port_ram.ram[input_addresses[3]]]

    def driver(self, user_input : list[complex]):
        data_fixedpoint = utils.Fixedpoint.complex_to_verilog_bits(user_input)
        self.selector.fill_input_data(data_fixedpoint, self.dual_port_ram.ram, self.address_generator.generate_input_addresses(self.state))
        self.dual_port_ram.dump()

        # self.fill_user_input(user_input)
        # self.data_to_ram()
        # input_addresses = self.address_generator.generate_input_addresses()
        # coefficients_list = self.generate_coefficients_list(input_addresses)
        # fft_block = fft.FFT4(coefficients_list)
        # fft_result = fft_block.count()
        # return fft_result


def main():
    fft_accelerator = FFTAccelerator()
    fft_accelerator_result = fft_accelerator.driver([1, 2, 3, 4])
    # print(fft_accelerator_result)

main()
