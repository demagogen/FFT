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

    @staticmethod
    def bits_to_complex_list(bit_array: list[int]) -> list[complex]:
        complex_list = []
        for i in range(0, len(bit_array), 32):
            chunk = bit_array[i:i + 32]
            if len(chunk) == 32:
                complex_list.append(Fixedpoint.bits_to_complex(chunk))
        return complex_list

    @staticmethod
    def nested_bits_to_complex(nested_list: list[list[int]]) -> list[complex]:
        complex_list = []
        for chunk in nested_list:
            if len(chunk) == 32:
                complex_list.append(Fixedpoint.bits_to_complex(chunk))
        return complex_list

    def split_128_to_32(bits_128: list[int]) -> list[list[int]]:
        if len(bits_128) != 128:
            raise ValueError(f"Expected 128 bits, but have {len(bits_128)}")
        return [bits_128[i:i + 32] for i in range(0, 128, 32)]

    def join_32_to_128(nested_bits: list[list[int]]) -> list[int]:
        if len(nested_bits) != 4:
            raise ValueError("Expected list of four")
        flat_list = []
        for chunk in nested_bits:
            flat_list.extend(chunk)
        return flat_list

    @staticmethod
    def float_to_fixed(value: float, fractional_bits: int = 10) -> int:
        scaled = int(round(value * (2 ** fractional_bits)))
        return scaled & 0xFFFF

class Dumps:
    def print_fixedpoint32(fixedpoint_list):
        for index in range(0, 32):
            print(fixedpoint_list[index], end="")
        print()

    def print_fixedpoint32_list4(fixedpoint_list_list):
        for string in range(0, 4):
            print("#", string, ": ", end="")
            for column in range(0, 32):
                print(fixedpoint_list_list[string][column], end="")
            print()

    def print_fixedpoint32_listn(fixedpoint_listn, strings : int):
        for string in range(0, strings):
            print("#", string, ": ", end="")
            for column in range(0, 32):
                print(fixedpoint_listn[string][column], end="")
            print()

    def print_fixedpoint32_listn_listm(fixedpoint_listn_listm, strings : int, columns : int):
        for string in range(0, strings):
            print("#", string, ": ", end="")
            for column in range(0, columns):
                print(fixedpoint_listn_listm[string][column], end="")
            print()

    def print_list(list, capacity):
        for index in range(0, capacity):
            print(list[index], end="")
        print()

    def ram_dump(ram):
        for strings in range(0, 4):
            print("#", strings, ": ", end="")
            for columns in range(0, 32):
                print(ram[strings * 32 + columns], end="")
            print()

    def print_nested_bits_as_complex(nested_list: list[list[int]]):
        for i, bits in enumerate(nested_list):
            re_part = bits[:16]
            im_part = bits[16:32]
            re_val = int("".join(map(str, re_part)), 2)
            im_val = int("".join(map(str, im_part)), 2)
            re_signed = re_val if re_val < 0x8000 else re_val - 0x10000
            im_signed = im_val if im_val < 0x8000 else im_val - 0x10000
            c_num = complex(re_signed, im_signed)
            print(f"Num{i}: {c_num}")

    def print_as_complex(bits: list[int]):
        if len(bits) != 32:
            print(f"Expected 32 bits, has {len(bits)}")
            return
        re_bits = bits[:16]
        im_bits = bits[16:32]
        re_val = int("".join(map(str, re_bits)), 2)
        im_val = int("".join(map(str, im_bits)), 2)
        re_signed = re_val if re_val < 0x8000 else re_val - 0x10000
        im_signed = im_val if im_val < 0x8000 else im_val - 0x10000
        print(complex(re_signed, im_signed))
