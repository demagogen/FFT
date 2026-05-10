import pytest
import math
from fft_accelerator.lut_with_twiddle_factors import LUTWithTwiddleFactors

lut = LUTWithTwiddleFactors()
amounts = [4, 16, 64, 256, 1024]

@pytest.mark.parametrize("amount", amounts)
def test_twiddle_generator_stages(amount):
    twiddles = lut.generate_twiddles(amount)
    assert len(twiddles) == int(math.log(amount, 4))

@pytest.mark.parametrize("amount", amounts)
def test_twiddle_generator_stage0_coeff(amount):
    twiddles = lut.generate_twiddles(amount)
    w02 = lut.twiddle_factor(0, 2)
    stages = int(math.log(amount, 4))
    assert twiddles[0][0][0] == w02

@pytest.mark.parametrize("amount", amounts)
def test_twiddle_generator_butterflies_per_stage(amount):
    twiddles = lut.generate_twiddles(amount)
    for stage in twiddles:
        assert len(stage) == amount // 4
