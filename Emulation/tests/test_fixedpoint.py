import pytest

from fixedpoint.fixedpoint import Fixedpoint

def test_positive_float():
    fp = Fixedpoint(0.75, 1, 0, 8)
    assert fp.raw_int == 96

def test_negative_float():
    fp = Fixedpoint(-0.5, 1, 0, 8)
    assert fp.raw_int == -64

def test_clipping_max():
    fp = Fixedpoint(2.0, 1, 0, 8)
    assert fp.raw_int == 127

def test_clipping_min():
    fp = Fixedpoint(-2.0, 1, 0, 8)
    assert fp.raw_int == -128

def test_from_complex():
    re, im = Fixedpoint.from_complex(0.5 + 0.25j, 1, 0, 8)
    assert re.raw_int == 64
    assert im.raw_int == 32

def test_invalid_sign():
    with pytest.raises(ValueError, match="with_sign must be 0 or 1"):
        Fixedpoint(0.5, with_sign=5, int_width=0, width=8)

def test_invalid_constraints():
    with pytest.raises(ValueError, match="Constraint failed"):
        Fixedpoint(0.5, 1, 10, 8)
