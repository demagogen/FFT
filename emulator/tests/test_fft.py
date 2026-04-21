import numpy
import pytest

from fft_accelerator.fft_accelerator import FFTAccelerator
from fixedpoint.fixedpoint import Fixedpoint
from fixedpoint.complex_fixedpoint import ComplexFixedpoint

PARAMS = {
    "with_sign": 1,
    "frac_width": 14,
    "width": 16,
    "saturate": False,
    "rounding": False,
}


low, high = -1.5555, 1.5555
test_vectors = numpy.random.uniform(
    low, high, size=(100, 4)
) + 1j * numpy.random.uniform(low, high, size=(100, 4))


@pytest.mark.parametrize("vector", test_vectors)
def test_fft_accelerator_individual(vector):
    fft = FFTAccelerator()

    scaled_vector = vector / 4
    inputs = [ComplexFixedpoint(v, **PARAMS) for v in scaled_vector]

    fft_result = fft.driver(inputs)

    expected = numpy.fft.fft(scaled_vector)

    actual = []
    for comp in fft_result:
        re = comp.real.raw_value / (1 << comp.frac_width)
        im = comp.imag.raw_value / (1 << comp.frac_width)
        actual.append(complex(re, im))

    assert numpy.allclose(actual, expected, atol=0.01)
