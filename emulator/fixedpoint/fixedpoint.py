import numpy


class Fixedpoint:
    def __init__(
        self, value, with_sign, frac_width, width, saturate=True, rounding=True
    ):
        self.width = width
        self.frac_width = frac_width
        self.with_sign = with_sign
        self.saturate = saturate
        self.rounding = rounding

        if isinstance(value, (int, numpy.integer)):
            raw = value
        else:

            raw = int(numpy.floor(value * (1 << self.frac_width)))

        self.raw_value = self._apply_hardware_limit(raw)
        self._update_nested_bits()

    def _apply_hardware_limit(self, raw):

        max_val = (1 << (self.width - 1)) - 1
        min_val = -(1 << (self.width - 1))
        mask = (1 << self.width) - 1

        if self.saturate:

            if raw > max_val:
                return max_val
            if raw < min_val:
                return min_val
            return raw
        else:

            raw &= mask
            if raw & (1 << (self.width - 1)):
                raw -= 1 << self.width
            return raw

    def _update_nested_bits(self):

        mask = (1 << self.width) - 1
        unsigned_raw = self.raw_value & mask

        bit_str = format(unsigned_raw, f"0{self .width }b")

        self.nested_bits = [int(b) for b in bit_str]

    def _create_from_raw(self, raw):

        obj = self.__class__.__new__(self.__class__)
        obj.width = self.width
        obj.frac_width = self.frac_width
        obj.with_sign = self.with_sign
        obj.saturate = self.saturate
        obj.rounding = self.rounding
        obj.raw_value = raw
        obj._update_nested_bits()
        return obj

    def __add__(self, other):
        return self._create_from_raw(
            self._apply_hardware_limit(self.raw_value + other.raw_value)
        )

    def __sub__(self, other):
        return self._create_from_raw(
            self._apply_hardware_limit(self.raw_value - other.raw_value)
        )

    def __mul__(self, other):
        res_large = self.raw_value * other.raw_value
        div = 1 << self.frac_width

        if self.rounding and self.frac_width > 0:

            res_raw = int(numpy.floor(res_large / div + 0.5))
        else:

            res_raw = int(res_large / div)

        return self._create_from_raw(self._apply_hardware_limit(res_raw))

    def __eq__(self, other):
        if not isinstance(other, Fixedpoint):
            return False
        return self.raw_value == other.raw_value

    def __repr__(self):
        return f"{self .raw_value /(1 <<self .frac_width )} (raw: {self .raw_value })"
