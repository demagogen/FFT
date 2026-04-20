import pytest

from fixedpoint.complex_fixedpoint import ComplexFixedpoint

PARAMS = {
    "with_sign": 1,
    "frac_width": 14,
    "width": 16,
    "saturate": True,
    "rounding": False,
}


def test_mul_hardware_accurate():
    params = {
        "with_sign": 1,
        "frac_width": 14,
        "width": 16,
        "rounding": True,
        "saturate": True,
    }
    cfp1 = ComplexFixedpoint(complex(0, -0.72), **params)
    cfp2 = ComplexFixedpoint(complex(0, 0.123), **params)

    result = cfp1 * cfp2

    expected_real_bits = [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
    expected_imag_bits = [0] * 16

    assert result.real.raw_value == 1451
    assert result.nested_bits == [expected_real_bits, expected_imag_bits]


def test_saturation_overflow():
    c1 = ComplexFixedpoint(complex(1.5, 0), **PARAMS)
    c2 = ComplexFixedpoint(complex(1.5, 0), **PARAMS)

    result = c1 * c2
    assert result.real.raw_value == 32767
    assert result.real.nested_bits == [0] + [1] * 15


def test_saturation_underflow():
    c1 = ComplexFixedpoint(complex(-1.5, 0), **PARAMS)
    c2 = ComplexFixedpoint(complex(1.5, 0), **PARAMS)

    result = c1 * c2
    assert result.real.raw_value == -32768
    assert result.real.nested_bits == [1] + [0] * 15


def test_complex_add_logic():
    c1 = ComplexFixedpoint(complex(0.5, 0.5), **PARAMS)
    c2 = ComplexFixedpoint(complex(0.75, -0.25), **PARAMS)

    result = c1 + c2
    assert result.real.raw_value == 20480
    assert result.imag.raw_value == 4096


def test_rounding_off():
    params_no_round = PARAMS.copy()
    params_no_round["rounding"] = False

    cfp1 = ComplexFixedpoint(complex(0, -0.72), **params_no_round)
    cfp2 = ComplexFixedpoint(complex(0, 0.123), **params_no_round)

    result = cfp1 * cfp2
    assert result.real.raw_value == 1450


def test_wrap_around_off():
    params_wrap = PARAMS.copy()
    params_wrap["saturate"] = False
    params_wrap["rounding"] = False

    c1 = ComplexFixedpoint(complex(1.5, 0), **params_wrap)
    c2 = ComplexFixedpoint(complex(1.5, 0), **params_wrap)

    result = c1 * c2
    assert result.real.raw_value == -28672
