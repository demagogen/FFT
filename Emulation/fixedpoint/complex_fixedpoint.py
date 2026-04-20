from fixedpoint.fixedpoint import Fixedpoint


class ComplexFixedpoint:
    def __init__(
        self, c_value, with_sign, frac_width, width, saturate=True, rounding=True
    ):
        self.with_sign = with_sign
        self.frac_width = frac_width
        self.width = width
        self.saturate = saturate
        self.rounding = rounding

        self.real = Fixedpoint(
            c_value.real, with_sign, frac_width, width, saturate, rounding
        )
        self.imag = Fixedpoint(
            c_value.imag, with_sign, frac_width, width, saturate, rounding
        )
        self.nested_bits = self.real.nested_bits + self.imag.nested_bits

    def _create_from_objects(self, real_obj, imag_obj):
        obj = self.__class__.__new__(self.__class__)
        obj.with_sign = self.with_sign
        obj.frac_width = self.frac_width
        obj.width = self.width
        obj.saturate = self.saturate
        obj.rounding = self.rounding
        obj.real = real_obj
        obj.imag = imag_obj
        obj.nested_bits = [obj.real.nested_bits, obj.imag.nested_bits]
        return obj

    def __add__(self, cfp):
        return self._create_from_objects(self.real + cfp.real, self.imag + cfp.imag)

    def __sub__(self, cfp):
        return self._create_from_objects(self.real - cfp.real, self.imag - cfp.imag)

    def __mul__(self, cfp):
        res_real = (self.real * cfp.real) - (self.imag * cfp.imag)
        res_imag = (self.real * cfp.imag) + (self.imag * cfp.real)
        return self._create_from_objects(res_real, res_imag)

    def __eq__(self, other):
        if not isinstance(other, ComplexFixedpoint):
            return False
        return self.real == other.real and self.imag == other.imag

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"ComplexFixedpoint({self.real}, {self.imag})"
