class FFT4:
    def __init__(self, polynomial: list[complex]):
        self.SIZE                  = 4
        self.polynomial            = [0j] * 4
        self.polynomial            = polynomial
        self.partition_polynomial1 = [0j] * 2
        self.partition_polynomial2 = [0j] * 2
        self.partition_vector1     = [0j] * 2
        self.partition_vector2     = [0j] * 2
        self.result_vector         = [0j] * 4

    def __repr__(self):
        return f"FFT4(polynomial='{self.polynomial}', size={self.SIZE})"

    def split(self):
        self.partition_polynomial1 = [self.polynomial[0], self.polynomial[2]]
        self.partition_polynomial2 = [self.polynomial[1], self.polynomial[3]]

    def dft(self):
        self.partition_vector1[0] = self.partition_polynomial1[0] + self.partition_polynomial1[1]
        self.partition_vector1[1] = self.partition_polynomial1[0] - self.partition_polynomial1[1]
        self.partition_vector2[0] = self.partition_polynomial2[0] + self.partition_polynomial2[1]
        self.partition_vector2[1] = self.partition_polynomial2[0] - self.partition_polynomial2[1]

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
