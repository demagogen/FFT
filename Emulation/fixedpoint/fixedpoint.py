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

        raw = int(value * (2**self.frac_width))
        self.raw_value = self._apply_hardware_limit(raw)
        self._update_nested_bits()

    def _update_nested_bits(self):
        mask = (1 << self.width) - 1
        unsigned_raw = self.raw_value & mask
        self.nested_bits = [
            (unsigned_raw >> i) & 1 for i in range(self.width - 1, -1, -1)
        ]

    def _apply_hardware_limit(self, raw):
        if self.saturate:
            max_val = (1 << (self.width - 1)) - 1
            min_val = -(1 << (self.width - 1))
            if raw > max_val:
                return max_val
            if raw < min_val:
                return min_val
            return raw
        else:
            mask = (1 << self.width) - 1
            raw &= mask
            if self.with_sign and (raw & (1 << (self.width - 1))):
                raw -= 1 << self.width
            return raw

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

    def __add__(self, fp):
        res_raw = self.raw_value + fp.raw_value
        return self._create_from_raw(self._apply_hardware_limit(res_raw))

    def __sub__(self, fp):
        res_raw = self.raw_value - fp.raw_value
        return self._create_from_raw(self._apply_hardware_limit(res_raw))

    def __mul__(self, fp):
        full_res = self.raw_value * fp.raw_value
        if self.rounding:
            full_res += 1 << (self.frac_width - 1)

        res_raw = int(full_res / (2**self.frac_width))
        return self._create_from_raw(self._apply_hardware_limit(res_raw))

    def __eq__(self, other):
        if not isinstance(other, Fixedpoint):
            return False
        return (
            self.raw_value == other.raw_value
            and self.width == other.width
            and self.frac_width == other.frac_width
            and self.with_sign == other.with_sign
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Fixedpoint(val={self.raw_value / (2**self.frac_width)}, raw={self.raw_value})"
