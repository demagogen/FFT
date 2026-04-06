class AddressGenerator:
    def __init__(self):

        # Constants
        self.SELECTOR_BUS_WIDTH      = 8
        self.WRITE_ADDRESS_BUS_WIDTH = 10
        self.READ_ADDRESS_BUS_WIDTH  = 10
        self.CONTROL_BLOCK_BUS_WIDTH = 20

        # Wires and busses
        self.start               = 0
        self.busy                = 0
        self.selector            = [0] * self.SELECTOR_BUS_WIDTH
        self.write_address       = [0] * self.WRITE_ADDRESS_BUS_WIDTH
        self.read_address        = [0] * self.READ_ADDRESS_BUS_WIDTH
        self.read_enable         = 0
        self.lut_twiddle_factors = 0
        self.from_control_block  = [0] * self.CONTROL_BLOCK_BUS_WIDTH

    # FFT4 managing
    # def send_coefficients_to_fft(self, ram : list[complex]):
        # if not ram:
            # print("Error: Try read data from empty data")
