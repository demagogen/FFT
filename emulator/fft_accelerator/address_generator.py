import math
from fft_accelerator.lut_with_twiddle_factors import LUTWithTwiddleFactors


class AddressGenerator:
    def generate_addresses(amount):
        radix = 4
        stages = int(math.log(amount, radix))
        addresses = []
        for stage in range(0, stages):
            stride = radix**stage
            group = radix * stride
            stage_addresses = []
            butterfly_input = []
            for base in range(0, amount, group):
                for offset in range(0, stride):
                    stage_addresses.append(
                        [
                            base + offset + 0 * stride,
                            base + offset + 1 * stride,
                            base + offset + 2 * stride,
                            base + offset + 3 * stride,
                        ]
                    )
            addresses.append(stage_addresses)
        return addresses
