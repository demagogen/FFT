from fixedpoint.fixedpoint import Fixedpoint
from fixedpoint.validator import validate

class ComplexFixedpoint:
    @validate
    def __init__(self, c_value: complex, with_sign: int, int_width: int, width: int):
        self.with_sign = with_sign
        self.int_width = int_width
        self.width = width
        self.real = Fixedpoint(c_value.real, with_sign, int_width, width)
        self.imag = Fixedpoint(c_value.imag, with_sign, int_width, width)

    @classmethod
    @validate
    def from_raw_bits(cls, bits: list[int], with_sign: int, int_width: int, width: int):
        if len(bits) != width * 2:
            raise ValueError(f"Expected {width * 2} bits, got {len(bits)}")

        re_raw_val = int("".join(map(str, bits[:width])), 2)
        im_raw_val = int("".join(map(str, bits[width:])), 2)

        def sign_extend(val, w):
            if not with_sign: return val
            return val if val < (1 << (w - 1)) else val - (1 << w)

        instance = cls(0j, with_sign, int_width, width)
        instance.real.raw_int = sign_extend(re_raw_val, width)
        instance.imag.raw_int = sign_extend(im_raw_val, width)
        return instance

    def to_complex(self) -> complex:
        return complex(self.real.to_float(), self.imag.to_float())

    @property
    def bits(self) -> list[int]:
        return self.real.bits + self.imag.bits

    def __repr__(self):
        return f"ComplexFixedpoint(value={self.to_complex()}, width={self.width}x2)"

    def __add__(self, other):
        return ComplexFixedpoint(self.to_complex() + other.to_complex(), self.with_sign, self.int_width, self.width)

    def __sub__(self, other):
        return ComplexFixedpoint(self.to_complex() - other.to_complex(), self.with_sign, self.int_width, self.width)

    def __mul__(self, other):
        return ComplexFixedpoint(self.to_complex() * other.to_complex(), self.with_sign, self.int_width, self.width)
