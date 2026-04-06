class LUTWithTwiddleFactors:
    def __init__(self):

        # Constants
        self.ADDRESS_GENERATOR_BUS_WIDTH = 10
        self.FFT_BUS_WIDTH               = 32
        self.ROM_BUS_WIDTH               = 32

        # Wire and buses
        self.address_generator = [0] * self.ADDRESS_GENERATOR_BUS_WIDTH
        self.fft               = [0] * self.FFT_BUS_WIDTH
        self.rom               = [0] * self.ROM_BUS_WIDTH
