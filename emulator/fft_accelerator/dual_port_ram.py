from fixedpoint.complex_fixedpoint import ComplexFixedpoint


class DualPortRAM:
    def __init__(self):

        self.WRITE_DATA_BUS_WIDTH = 8 * 16
        self.WRITE_ADDRESS_BUS_WIDTH = 10
        self.READ_ADDRESS_BUS_WIDTH = 10
        self.READ_DATA_BUS_WIDTH = 8 * 16
        self.RAM_CAPACITY = 8 * 16
        self.RAM_STRINGS = 4
        self.RAM_COLUMNS = 32
        self.COEFFICIENT_WIDTH = 32

        self.write_data = [0] * self.WRITE_DATA_BUS_WIDTH
        self.write_enable = 0
        self.write_address = [0] * self.WRITE_ADDRESS_BUS_WIDTH
        self.read_address = [0] * self.READ_ADDRESS_BUS_WIDTH
        self.read_data = [0] * self.READ_DATA_BUS_WIDTH

        self.ram = [ComplexFixedpoint] * 1024
