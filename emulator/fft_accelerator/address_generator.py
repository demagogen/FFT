class AddressGenerator:
    def __init__(self):

        self.SELECTOR_BUS_WIDTH = 8
        self.WRITE_ADDRESS_BUS_WIDTH = 10
        self.READ_ADDRESS_BUS_WIDTH = 10
        self.CONTROL_BLOCK_BUS_WIDTH = 20

        self.start = 0
        self.busy = 0
        self.selector = [0] * self.SELECTOR_BUS_WIDTH
        self.write_address = [0] * self.WRITE_ADDRESS_BUS_WIDTH
        self.read_address = [0] * self.READ_ADDRESS_BUS_WIDTH
        self.read_enable = 0
        self.lut_twiddle_factors = 0
        self.from_control_block = [0] * self.CONTROL_BLOCK_BUS_WIDTH

    def generate_input_addresses(self, state=None):
        return [0, 1, 2, 3]

    def generate_addresses_for_fft_input(self, state=None):
        return [0, 2, 1, 3]
