import pytest

from fixedpoint.fixedpoint import Fixedpoint


def test_signed_raw_value():
    value = 12.34
    fp = Fixedpoint(12.34, 1, 10, 15)
    assert fp.raw_value == 12636


def test_signed_nested_bits():
    value = 12.34
    fp = Fixedpoint(12.34, 1, 10, 15)
    assert fp.nested_bits == [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0]


def test_signed_raw_add():
    value1 = 15.6
    value2 = -234.2
    params = {"with_sign": 1, "frac_width": 10, "width": 20}
    fp1 = Fixedpoint(value1, **params)
    fp2 = Fixedpoint(value2, **params)
    res = fp1 + fp2
    expected_raw = fp1.raw_value + fp2.raw_value

    assert res.raw_value == expected_raw
