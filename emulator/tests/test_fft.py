import numpy
import pytest

from fft_accelerator.fft import FFT
from fft_accelerator.lut_with_twiddle_factors import LUTWithTwiddleFactors
from fixedpoint.complex_fixedpoint import ComplexFixedpoint
from tests.params import (
    PARAMS,
    PARAMS_ROUNDING,
    PARAMS_SATURATE,
    PARAMS_SATURATE_ROUNDING,
)


def fixedpoint_to_complex(data):

    actual = []

    for comp in data:

        re = comp.real.raw_value / (1 << comp.frac_width)
        im = comp.imag.raw_value / (1 << comp.frac_width)

        actual.append(complex(re, im))

    return actual


low, high = -1.5555, 1.5555
test_vector_radix2 = numpy.random.uniform(
    low, high, size=(100, 2)
) + 1j * numpy.random.uniform(low, high, size=(100, 2))
test_vector_radix4 = numpy.random.uniform(
    low, high, size=(100, 4)
) + 1j * numpy.random.uniform(low, high, size=(100, 4))
test_vector_radix8 = numpy.random.uniform(
    low, high, size=(100, 8)
) + 1j * numpy.random.uniform(low, high, size=(100, 8))
test_vector_radix16 = numpy.random.uniform(
    low, high, size=(100, 16)
) + 1j * numpy.random.uniform(low, high, size=(100, 16))

elements_amounts = [4, 5, 6, 7, 8]

test_vector_radix64 = numpy.random.uniform(
    low, high, size=(100, 64)
) + 1j * numpy.random.uniform(low, high, size=(100, 64))


test_vector_radix1024 = numpy.random.uniform(
    low, high, size=(10, 1024)
) + 1j * numpy.random.uniform(low, high, size=(10, 1024))


@pytest.mark.parametrize("vector", test_vector_radix4)
def test_fft_accelerator_individual(vector):
    fft = FFT()
    scaled_vector = vector / 4
    inputs = [ComplexFixedpoint(v, **PARAMS) for v in scaled_vector]
    fft_result = fft.radix4(inputs)
    expected = numpy.fft.fft(scaled_vector)
    actual = []
    for comp in fft_result:
        re = comp.real.raw_value / (1 << comp.frac_width)
        im = comp.imag.raw_value / (1 << comp.frac_width)
        actual.append(complex(re, im))
    assert numpy.allclose(actual, expected, atol=0.001)


@pytest.mark.parametrize("vector", test_vector_radix4)
def test_fft_accelerator_saturate(vector):
    fft = FFT()
    scaled_vector = vector / 4
    inputs = [ComplexFixedpoint(v, **PARAMS_SATURATE) for v in scaled_vector]
    fft_result = fft.radix4(inputs)
    expected = numpy.fft.fft(scaled_vector)
    actual = []
    for comp in fft_result:
        re = comp.real.raw_value / (1 << comp.frac_width)
        im = comp.imag.raw_value / (1 << comp.frac_width)
        actual.append(complex(re, im))
    assert numpy.allclose(actual, expected, atol=0.001)


@pytest.mark.parametrize("vector", test_vector_radix4)
def test_fft_accelerator_rounding(vector):
    fft = FFT()
    scaled_vector = vector / 4
    inputs = [ComplexFixedpoint(v, **PARAMS_ROUNDING) for v in scaled_vector]
    fft_result = fft.radix4(inputs)
    expected = numpy.fft.fft(scaled_vector)
    actual = []
    for comp in fft_result:
        re = comp.real.raw_value / (1 << comp.frac_width)
        im = comp.imag.raw_value / (1 << comp.frac_width)
        actual.append(complex(re, im))
    assert numpy.allclose(actual, expected, atol=0.001)


@pytest.mark.parametrize("vector", test_vector_radix4)
def test_fft_accelerator_saturate_rounding(vector):
    fft = FFT()
    scaled_vector = vector / 4
    inputs = [ComplexFixedpoint(v, **PARAMS_SATURATE_ROUNDING) for v in scaled_vector]
    fft_result = fft.radix4(inputs)
    expected = numpy.fft.fft(scaled_vector)
    actual = []
    for comp in fft_result:
        re = comp.real.raw_value / (1 << comp.frac_width)
        im = comp.imag.raw_value / (1 << comp.frac_width)
        actual.append(complex(re, im))
    assert numpy.allclose(actual, expected, atol=0.001)


@pytest.mark.parametrize("vector", test_vector_radix2)
def test_fft_accelerator_radix2(vector):
    scaled_vector = vector / 2
    inputs = [ComplexFixedpoint(v, **PARAMS_SATURATE_ROUNDING) for v in scaled_vector]
    save_hex_file(inputs, "../design/testbenches/tests/radix2_inputs.txt")
    fft = FFT()
    fft_result = fft.radix2(inputs, (0, 0))
    expected = numpy.fft.fft(scaled_vector)
    actual = []
    for comp in fft_result:
        re = comp.real.raw_value / (1 << comp.frac_width)
        im = comp.imag.raw_value / (1 << comp.frac_width)
        actual.append(complex(re, im))
    save_hex_file(fft_result, "../design/testbenches/tests/radix2_answers.txt")
    assert numpy.allclose(actual, expected, atol=0.001)


def save_hex_file(data_list, filename):
    import os

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a") as f:
        for val in data_list:
            re_hex = format(val.real.raw_value & 0xFFFF, "04x")
            im_hex = format(val.imag.raw_value & 0xFFFF, "04x")
            f.write(f"{re_hex}{im_hex}\n")


@pytest.mark.parametrize("vector", test_vector_radix8)
def test_fft_accelerator_radix8(vector):
    scaled_vector = vector / 8
    inputs = [ComplexFixedpoint(v, **PARAMS_SATURATE_ROUNDING) for v in scaled_vector]
    fft = FFT()
    fft_result = fft.radix8(inputs, (0, 0))
    expected = numpy.fft.fft(scaled_vector)
    actual = []
    for comp in fft_result:
        re = comp.real.raw_value / (1 << comp.frac_width)
        im = comp.imag.raw_value / (1 << comp.frac_width)
        actual.append(complex(re, im))
    assert numpy.allclose(actual, expected, atol=0.001)


@pytest.mark.parametrize("vector", test_vector_radix4)
def test_driver_radix4_fft4(vector):
    fft = FFT()
    scaled_vector = vector
    inputs = [ComplexFixedpoint(v, **PARAMS_SATURATE_ROUNDING) for v in scaled_vector]
    result = fft.driver_radix4(inputs)
    actual = fixedpoint_to_complex(result)
    expected = numpy.fft.fft(scaled_vector) / 4
    assert numpy.allclose(actual, expected, atol=0.001)


@pytest.mark.parametrize("amount", [16, 64, 256, 1024])
def test_driver_radix4_impulse(amount):
    fft = FFT()
    vector = numpy.zeros(amount, dtype=complex)
    vector[0] = 1.0
    scaled_vector = vector
    inputs = [ComplexFixedpoint(v, **PARAMS_SATURATE_ROUNDING) for v in scaled_vector]
    reordered_inputs = fft.reorder_radix4(inputs)
    result = fft.driver_radix4(reordered_inputs)
    actual = fixedpoint_to_complex(result)
    expected = numpy.fft.fft(scaled_vector) / amount
    assert numpy.allclose(actual, expected, atol=0.001)


@pytest.mark.parametrize("vector", test_vector_radix16)
def test_driver_radix4_fft16(vector):
    fft = FFT()
    scaled_vector = vector
    inputs = [ComplexFixedpoint(v, **PARAMS_SATURATE_ROUNDING) for v in scaled_vector]
    inputs = fft.reorder_radix4(inputs)
    result = fft.driver_radix4(inputs)
    actual = fixedpoint_to_complex(result)
    expected = numpy.fft.fft(scaled_vector) / 16
    assert numpy.allclose(actual, expected, atol=0.001)


def test_twiddles_stage1_fft16():
    twiddles = LUTWithTwiddleFactors.generate_twiddles(16)
    stage1 = twiddles[1]
    expected = [
        [0, 0, 0, 0],
        [0, 1, 2, 3],
        [0, 2, 4, 6],
        [0, 3, 6, 9],
    ]
    for butterfly_index in range(4):
        for branch in range(4):
            actual = stage1[butterfly_index][branch]
            reference = LUTWithTwiddleFactors.twiddle_factor(
                expected[butterfly_index][branch], 16
            )
            assert actual == reference


@pytest.mark.parametrize("vector", test_vector_radix1024)
def test_driver_radix4_fft1024(vector):
    fft = FFT()
    scaled_vector = vector
    inputs = [ComplexFixedpoint(v, **PARAMS_SATURATE_ROUNDING) for v in scaled_vector]
    reordered_inputs = fft.reorder_radix4(inputs)
    result = fft.driver_radix4(reordered_inputs)
    actual = fixedpoint_to_complex(result)
    expected = numpy.fft.fft(scaled_vector) / 1024
    assert numpy.allclose(actual, expected, atol=0.001)
