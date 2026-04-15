from fixedpoint.validator import validate

class Fixedpoint:

    @staticmethod
    @validate
    def __init__(self, value: float, with_sign: int, int_width: int, width: int):
        self.with_sign = with_sign
        self.int_width = int_width
        self.width = width
        self.raw_int = self._convert(value)

    @staticmethod
    @validate
    def _convert(self, float_value: float) -> int:
        fractional_bits = self.width - self.with_sign - self.int_width
        tmp = int(round(float_value * (2 ** fractional_bits)))

        max_limit = 1 << (self.width - self.with_sign)
        return max(-max_limit, min(max_limit - 1, tmp))

    @staticmethod
    @validate
    def __repr__(self):
        return f"Fixedpoint(raw={self.raw_int}, width={self.width})"

    @classmethod
    @validate
    def from_complex(cls, c_value: complex, with_sign: int, int_width: int, width: int):
        real_part = cls(c_value.real, with_sign, int_width, width)
        imag_part = cls(c_value.imag, with_sign, int_width, width)
        return real_part, imag_part
