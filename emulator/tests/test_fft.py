import numpy
import pytest
from fixedpoint.complex_fixedpoint import ComplexFixedpoint
from fft_accelerator.fft import FFT
from tests.params import PARAMS
from tests.params import PARAMS_SATURATE
from tests.params import PARAMS_ROUNDING
from tests.params import PARAMS_SATURATE_ROUNDING

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


@pytest.mark.parametrize("vector", test_vector_radix16)
def test_fft_accelerator_radix16(vector):
    scaled_vector = vector / 16
    inputs = [ComplexFixedpoint(v, **PARAMS_SATURATE_ROUNDING) for v in scaled_vector]
    fft = FFT()
    fft_result = fft.radix16(inputs, (0, 0))
    expected = numpy.fft.fft(scaled_vector)
    actual = []
    for comp in fft_result:
        re = comp.real.raw_value / (1 << comp.frac_width)
        im = comp.imag.raw_value / (1 << comp.frac_width)
        actual.append(complex(re, im))
    perm = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

    reordered_actual = [actual[p] for p in perm]
    for i in range(0, 16):
        print(reordered_actual[i], " -- ", expected[i])
    assert numpy.allclose(reordered_actual, expected, atol=0.001)


# @pytest.mark.parametrize("amount", elements_amounts)
# def test_address_generator(amount: int):
# for i in range(4, 16):
# addresses = FFT.gen_addr(i)
# print("Addresses ", i, ":", addresses)
# assert 0
