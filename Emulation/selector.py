class Selector:
    def __init__(self):

        # Constants
        self.ADDRESS_GENERATOR_BUS_WIDTH = 8
        self.WRITE_DATA_BUS_WIDTH        = 8 * 16
        self.SCALE_BUS_WIDTH             = 8 * 16

        # Wires and buses
        self.address_generator = [0] * self.ADDRESS_GENERATOR_BUS_WIDTH
        self.write_data        = [0] * self.WRITE_DATA_BUS_WIDTH
        self.write_enable      = 0
        self.scale             = [0] * self.SCALE_BUS_WIDTH
