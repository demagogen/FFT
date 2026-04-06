class Fixedpoint:
    def complex_to_verilog_bits(complex_nums: list[complex]) -> list[int]:
        bit_array = []
        for complex in complex_nums:
            real      = int(complex.real) & 0xFFFF
            imaginary = int(complex.imag) & 0xFFFF
            for value in [real, imaginary]:
                bits = [int(bit) for bit in f"{value:016b}"]
                bit_array.extend(bits)
        return bit_array

    def to_signed(value):
        return value if value < 0x8000 else value - 0x10000

    def verilog_style_add(value1: complex, value2: complex) -> complex:
        result_real      = (int(value1.real) + int(value2.real)) & 0xFFFF
        result_imaginary = (int(value1.imag) + int(value2.imag)) & 0xFFFF
        return complex(Fixedpoint.to_signed(result_real), Fixedpoint.to_signed(result_imaginary))

    def verilog_style_mult(value1: complex, value2: complex) -> complex:
        result_real      = int(value1.real) * int(value2.real) - int(value1.imag) * int(value2.imag)
        result_imaginary = int(value1.real) * int(value2.imag) + int(value1.imag) * int(value2.real)
        return complex(result_real & 0xFFFF, result_imaginary & 0xFFFF)
