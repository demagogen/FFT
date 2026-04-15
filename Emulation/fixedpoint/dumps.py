class Fixedpoint:
    TOTAL_BITS = 16
    FRAC_BITS = 10
    MASK = (1 << TOTAL_BITS) - 1
    OFFSET = 1 << (TOTAL_BITS - 1)

    @classmethod
    def to_fixed(cls, value: float | int) -> int:
        if isinstance(value, float):
            return int(round(value * (1 << cls.FRAC_BITS))) & cls.MASK
        return int(value) & cls.MASK

    @classmethod
    def to_signed(cls, value: int) -> int:
        value &= cls.MASK
        return value if value < cls.OFFSET else value - (1 << cls.TOTAL_BITS)

    @staticmethod
    def _to_bits(value: int) -> list[int]:
        return [int(b) for b in f"{int(value) & 0xFFFF:016b}"]

    @staticmethod
    def make_verilog_complex(real: float | int, imag: float | int) -> list[int]:
        return Fixedpoint._to_bits(Fixedpoint.to_fixed(real)) + \
               Fixedpoint._to_bits(Fixedpoint.to_fixed(imag))

    @staticmethod
    def make_verilog_complex_raw(real_int: int, imag_int: int) -> list[int]:
        return Fixedpoint._to_bits(real_int) + Fixedpoint._to_bits(imag_int)

    @staticmethod
    def complex_to_32bit_list(re: float | int, im: float | int) -> list[int]:
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
        re_val = Fixedpoint.to_signed(int("".join(map(str, bit_array[:16])), 2))
        im_val = Fixedpoint.to_signed(int("".join(map(str, bit_array[16:32])), 2))
        return complex(re_val, im_val)

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
        return [Fixedpoint.bits_to_complex(chunk) for chunk in nested_list if len(chunk) == 32]

    @classmethod
    def verilog_style_add(cls, v1: complex, v2: complex) -> complex:
        re = (int(v1.real) + int(v2.real)) & cls.MASK
        im = (int(v1.imag) + int(v2.imag)) & cls.MASK
        return complex(cls.to_signed(re), cls.to_signed(im))

    @classmethod
    def verilog_style_sub(cls, v1: complex, v2: complex) -> complex:
        re = (int(v1.real) - int(v2.real)) & cls.MASK
        im = (int(v1.imag) - int(v2.imag)) & cls.MASK
        return complex(cls.to_signed(re), cls.to_signed(im))

    @classmethod
    def verilog_style_mult(cls, v1: complex, v2: complex) -> complex:
        re_full = (int(v1.real) * int(v2.real)) - (int(v1.imag) * int(v2.imag))
        im_full = (int(v1.real) * int(v2.imag)) + (int(v1.imag) * int(v2.real))
        re = (re_full + (1 << (cls.FRAC_BITS - 1))) >> cls.FRAC_BITS
        im = (im_full + (1 << (cls.FRAC_BITS - 1))) >> cls.FRAC_BITS
        return complex(cls.to_signed(re & cls.MASK), cls.to_signed(im & cls.MASK))

    @staticmethod
    def add_bits_32(bits1: list[int], bits2: list[int]) -> list[int]:
        c1 = Fixedpoint.bits_to_complex(bits1)
        c2 = Fixedpoint.bits_to_complex(bits2)
        res = Fixedpoint.verilog_style_add(c1, c2)
        return Fixedpoint.make_verilog_complex_raw(res.real, res.imag)

    @staticmethod
    def sub_bits_32(bits1: list[int], bits2: list[int]) -> list[int]:
        c1 = Fixedpoint.bits_to_complex(bits1)
        c2 = Fixedpoint.bits_to_complex(bits2)
        res = Fixedpoint.verilog_style_sub(c1, c2)
        return Fixedpoint.make_verilog_complex_raw(res.real, res.imag)

    @staticmethod
    def mult_bits_32(bits1: list[int], bits2: list[int]) -> list[int]:
        c1 = Fixedpoint.bits_to_complex(bits1)
        c2 = Fixedpoint.bits_to_complex(bits2)
        res = Fixedpoint.verilog_style_mult(c1, c2)
        return Fixedpoint.make_verilog_complex_raw(res.real, res.imag)

    @staticmethod
    def split_128_to_32(bits_128: list[int]) -> list[list[int]]:
        if len(bits_128) != 128:
            raise ValueError(f"Expected 128 bits, but have {len(bits_128)}")
        return [bits_128[i:i + 32] for i in range(0, 128, 32)]

    @staticmethod
    def join_32_to_128(nested_bits: list[list[int]]) -> list[int]:
        if len(nested_bits) != 4:
            raise ValueError("Expected list of four")
        flat_list = []
        for chunk in nested_bits:
            flat_list.extend(chunk)
        return flat_list


class dumps:
    def print_fixedpoint32_nested_bytes_list4(fixedpoint_list4):
        for index in range(0, 4):
            print("#", index, ": ", end="")
            for columns in range(0, 32):
                print(fixedpoint_list4[index * 32 + columns], end="")
            print()

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
