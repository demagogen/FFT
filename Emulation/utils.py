class Fixedpoint:
    @staticmethod
    def to_signed(value: int) -> int:
        value &= 0xFFFF
        return value if value < 0x8000 else value - 0x10000

    @staticmethod
    def make_verilog_complex(real: int, imag: int) -> list[int]:
        bits_re = [int(b) for b in f"{int(real) & 0xFFFF:016b}"]
        bits_im = [int(b) for b in f"{int(imag) & 0xFFFF:016b}"]
        return bits_re + bits_im

    @staticmethod
    def complex_to_32bit_list(re: int, im: int) -> list[int]:
        return Fixedpoint.make_verilog_complex(re, im)

    @staticmethod
    def complex_to_verilog_bits(complex_nums: list[complex]) -> list[int]:
        bit_array = []
        for c in complex_nums:
            bit_array.extend(Fixedpoint.make_verilog_complex(c.real, c.imag))
        return bit_array

    @staticmethod
    def bits_to_complex(bit_array: list[int]) -> complex:
        if len(bit_array) != 32:
            raise ValueError("Expected 32 bits")

        re_str = "".join(map(str, bit_array[:16]))
        im_str = "".join(map(str, bit_array[16:32]))

        re_val = Fixedpoint.to_signed(int(re_str, 2))
        im_val = Fixedpoint.to_signed(int(im_str, 2))
        return complex(re_val, im_val)

    @staticmethod
    def verilog_style_add(v1: complex, v2: complex) -> complex:
        re = (int(v1.real) + int(v2.real)) & 0xFFFF
        im = (int(v1.imag) + int(v2.imag)) & 0xFFFF
        return complex(Fixedpoint.to_signed(re), Fixedpoint.to_signed(im))

    @staticmethod
    def verilog_style_sub(v1: complex, v2: complex) -> complex:
        re = (int(v1.real) - int(v2.real)) & 0xFFFF
        im = (int(v1.imag) - int(v2.imag)) & 0xFFFF
        return complex(Fixedpoint.to_signed(re), Fixedpoint.to_signed(im))

    @staticmethod
    def verilog_style_mult(v1: complex, v2: complex) -> complex:
        re = (int(v1.real) * int(v2.real)) - (int(v1.imag) * int(v2.imag))
        im = (int(v1.real) * int(v2.imag)) + (int(v1.imag) * int(v2.real))
        return complex(Fixedpoint.to_signed(re & 0xFFFF), Fixedpoint.to_signed(im & 0xFFFF))

    @staticmethod
    def add_bits_32(bits1: list[int], bits2: list[int]) -> list[int]:
        c1 = Fixedpoint.bits_to_complex(bits1)
        c2 = Fixedpoint.bits_to_complex(bits2)
        res = Fixedpoint.verilog_style_add(c1, c2)
        return Fixedpoint.make_verilog_complex(res.real, res.imag)

    @staticmethod
    def sub_bits_32(bits1: list[int], bits2: list[int]) -> list[int]:
        c1 = Fixedpoint.bits_to_complex(bits1)
        c2 = Fixedpoint.bits_to_complex(bits2)
        res = Fixedpoint.verilog_style_sub(c1, c2)
        return Fixedpoint.make_verilog_complex(res.real, res.imag)

    @staticmethod
    def mult_bits_32(bits1: list[int], bits2: list[int]) -> list[int]:
        c1 = Fixedpoint.bits_to_complex(bits1)
        c2 = Fixedpoint.bits_to_complex(bits2)
        res = Fixedpoint.verilog_style_mult(c1, c2)
        return Fixedpoint.make_verilog_complex(res.real, res.imag)
