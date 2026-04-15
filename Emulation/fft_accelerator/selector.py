class Selector:
    def __init__(self):

        # Constants
        self.INPUT_BUS_WIDTH             = 8 * 16 # 16 bits for real and 16 bits for imaginary part in fixedpoint. Bit reversed
        self.ADDRESS_GENERATOR_BUS_WIDTH = 8
        self.WRITE_DATA_BUS_WIDTH        = 8 * 16
        self.SCALE_BUS_WIDTH             = 8 * 16

        # Wires and buses
        self.address_generator = [0] * self.ADDRESS_GENERATOR_BUS_WIDTH
        self.write_data        = [0] * self.WRITE_DATA_BUS_WIDTH
        self.write_enable      = 0
        self.scale             = [0] * self.SCALE_BUS_WIDTH

    def fill_input_data(self, input_data : list[complex], ram : list[complex], agu_addresses : list[int]):
        if len(input_data) != self.INPUT_BUS_WIDTH:
            print("Not correct amount of bits for selector input data")
        else:
            for index in range(0, len(input_data)):
                ram[index] = input_data[index]
