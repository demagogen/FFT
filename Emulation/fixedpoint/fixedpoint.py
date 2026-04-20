import numpy

from fixedpoint.validator import validate_init

class Fixedpoint:
    @validate_init
    def __init__(self, value: float, with_sign: int, frac_width: int, width: int):
        self.width = width
        self.frac_width = frac_width
        self.with_sign = with_sign

        raw = int(numpy.round(value * (2 ** self.frac_width)))
        self.raw_value = self._apply_hardware_limit(raw)
        self._update_nested_bits()

    def _update_nested_bits(self):
        mask = (1 << self.width) - 1
        unsigned_raw = self.raw_value & mask
        self.nested_bits = [(unsigned_raw >> i) & 1 for i in range(self.width - 1, -1, -1)]

    def _apply_hardware_limit(self, raw):
        mask = (1 << self.width) - 1
        raw &= mask
        if self.with_sign and (raw & (1 << (self.width - 1))):
            raw -= (1 << self.width)
        return raw

    def _create_from_raw(self, raw):
        obj = self.__class__.__new__(self.__class__)
        obj.width = self.width
        obj.frac_width = self.frac_width
        obj.with_sign = self.with_sign
        obj.raw_value = raw
        obj._update_nested_bits()
        return obj

    def __add__(self, fp: 'Fixedpoint'):
        res_raw = self.raw_value + fp.raw_value
        return self._create_from_raw(self._apply_hardware_limit(res_raw))

    def __sub__(self, fp: 'Fixedpoint'):
        res_raw = self.raw_value - fp.raw_value
        return self._create_from_raw(self._apply_hardware_limit(res_raw))

    def __mul__(self, fp: 'Fixedpoint'):
        full_res = self.raw_value * fp.raw_value
        res_raw = full_res >> self.frac_width
        return self._create_from_raw(self._apply_hardware_limit(res_raw))

    def __truediv__(self, fp: 'Fixedpoint'):
        if fp.raw_value == 0:
            raise ZeroDivisionError
        res_raw = (self.raw_value << self.frac_width) // fp.raw_value
        return self._create_from_raw(self._apply_hardware_limit(res_raw))

    def __eq__(self, other):
        if not isinstance(other, Fixedpoint):
            return False
        if (self.width != other.width or
            self.frac_width != other.frac_width or
            self.with_sign != other.with_sign):
            return False
        return abs(self.raw_value - other.raw_value) <= 1

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Fixedpoint(val={self.raw_value / (2**self.frac_width)}, raw={self.raw_value})"
