class FFT4:
    def __init__(self, polynomial=None):

        # Constants
        self.RAM_INPUT_BUS_WIDTH                = 16 * 8
        self.LUT_WITH_TWIDDLE_FACTORS_BUS_WIDTH = 16 * 2
        self.OUTPUT_BUS_WIDTH                   = 16 * 8

        # Wires and busses
        self.ram_input                = [0] * self.RAM_INPUT_BUS_WIDTH
        self.lut_with_twiddle_factors = [0] * self.LUT_WITH_TWIDDLE_FACTORS_BUS_WIDTH
        self.output                   = [0] * self.OUTPUT_BUS_WIDTH

    def __repr__(self):
        return f"FFT4(polynomial='{self.polynomial}', size={self.SIZE})"

    def split(self):
        self.partition_polynomial1 = [self.polynomial[0], self.polynomial[2]]
        self.partition_polynomial2 = [self.polynomial[1], self.polynomial[3]]

    def dft(self):
        self.partition_vector1[0] = self.partition_polynomial1[0] + self.partition_polynomial1[1] # 0
        self.partition_vector1[1] = self.partition_polynomial1[0] - self.partition_polynomial1[1] # 2
        self.partition_vector2[0] = self.partition_polynomial2[0] + self.partition_polynomial2[1] # 1
        self.partition_vector2[1] = self.partition_polynomial2[0] - self.partition_polynomial2[1] # 3

    def synchronize(self):
        w40 = complex( 1,  0)
        w41 = complex( 0,  1)
        self.result_vector[0] = self.partition_vector1[0] + w40 * self.partition_vector2[0]
        self.result_vector[3] = self.partition_vector1[1] + w41 * self.partition_vector2[1]
        self.result_vector[2] = self.partition_vector1[0] - w40 * self.partition_vector2[0]
        self.result_vector[1] = self.partition_vector1[1] - w41 * self.partition_vector2[1]
        return self.result_vector

    def count(self):
        self.split()
        self.dft()
        return self.synchronize()

    def fft_driver(self, coefficients_from_ram : list, twiddle_factor1 : complex, twiddle_factor2 : complex):


    # def fft_count_iteration(self, ):
