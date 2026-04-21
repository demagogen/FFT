from fixedpoint.complex_fixedpoint import ComplexFixedpoint


class Selector:
    def __init__(self):

        self.INPUT_BUS_WIDTH = 8 * 16
        self.ADDRESS_GENERATOR_BUS_WIDTH = 8
        self.WRITE_DATA_BUS_WIDTH = 8 * 16
        self.SCALE_BUS_WIDTH = 8 * 16

        self.address_generator = [0] * self.ADDRESS_GENERATOR_BUS_WIDTH
        self.write_data = [0] * self.WRITE_DATA_BUS_WIDTH
        self.write_enable = 0
        self.scale = [0] * self.SCALE_BUS_WIDTH

    def data_to_ram(
        self, input_cfp: list[ComplexFixedpoint], ram: list[ComplexFixedpoint]
    ):
        for index in range(0, len(input_cfp)):
            ram[index] = input_cfp[index]
