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
    assert twiddles[0][0][0] == w02


@pytest.mark.parametrize("amount", amounts)
def test_twiddle_generator_butterflies_per_stage(amount):
    twiddles = lut.generate_twiddles(amount)
    for stage in twiddles:
        assert len(stage) == amount // 4


def test_twiddle_generator_fft16_stage1_exact():

    twiddles = lut.generate_twiddles(16)

    stage1 = twiddles[1]

    assert stage1[0][0] == lut.twiddle_factor(0, 16)
    assert stage1[0][1] == lut.twiddle_factor(0, 16)
    assert stage1[0][2] == lut.twiddle_factor(0, 16)
    assert stage1[0][3] == lut.twiddle_factor(0, 16)

    assert stage1[1][0] == lut.twiddle_factor(0, 16)
    assert stage1[1][1] == lut.twiddle_factor(1, 16)
    assert stage1[1][2] == lut.twiddle_factor(2, 16)
    assert stage1[1][3] == lut.twiddle_factor(3, 16)

    assert stage1[2][0] == lut.twiddle_factor(0, 16)
    assert stage1[2][1] == lut.twiddle_factor(2, 16)
    assert stage1[2][2] == lut.twiddle_factor(4, 16)
    assert stage1[2][3] == lut.twiddle_factor(6, 16)

    assert stage1[3][0] == lut.twiddle_factor(0, 16)
    assert stage1[3][1] == lut.twiddle_factor(3, 16)
    assert stage1[3][2] == lut.twiddle_factor(6, 16)
    assert stage1[3][3] == lut.twiddle_factor(9, 16)


def test_twiddle_generator_fft64_stage1_exact():
    twiddles = lut.generate_twiddles(64)

    stage1 = twiddles[1]

    assert stage1[0][1] == lut.twiddle_factor(0, 64)
    assert stage1[0][2] == lut.twiddle_factor(0, 64)
    assert stage1[0][3] == lut.twiddle_factor(0, 64)

    assert stage1[1][1] == lut.twiddle_factor(4, 64)
    assert stage1[1][2] == lut.twiddle_factor(8, 64)
    assert stage1[1][3] == lut.twiddle_factor(12, 64)

    assert stage1[2][1] == lut.twiddle_factor(8, 64)
    assert stage1[2][2] == lut.twiddle_factor(16, 64)
    assert stage1[2][3] == lut.twiddle_factor(24, 64)

    assert stage1[3][1] == lut.twiddle_factor(12, 64)
    assert stage1[3][2] == lut.twiddle_factor(24, 64)
    assert stage1[3][3] == lut.twiddle_factor(36, 64)


def test_twiddle_generator_fft256_stage2_exact():

    twiddles = lut.generate_twiddles(256)

    stage2 = twiddles[2]

    assert stage2[1][1] == lut.twiddle_factor(4, 256)
    assert stage2[1][2] == lut.twiddle_factor(8, 256)
    assert stage2[1][3] == lut.twiddle_factor(12, 256)

    assert stage2[5][1] == lut.twiddle_factor(20, 256)
    assert stage2[5][2] == lut.twiddle_factor(40, 256)
    assert stage2[5][3] == lut.twiddle_factor(60, 256)


def test_fft1024_stage4_exact():

    twiddles = lut.generate_twiddles(1024)

    stage4 = twiddles[4]

    assert stage4[1][1] == lut.twiddle_factor(1, 1024)
    assert stage4[1][2] == lut.twiddle_factor(2, 1024)
    assert stage4[1][3] == lut.twiddle_factor(3, 1024)

    assert stage4[100][1] == lut.twiddle_factor(100, 1024)
    assert stage4[100][2] == lut.twiddle_factor(200, 1024)
    assert stage4[100][3] == lut.twiddle_factor(300, 1024)


@pytest.mark.parametrize("amount", amounts)
def test_twiddle_formula(amount):

    twiddles = lut.generate_twiddles(amount)

    radix = 4

    stages = int(math.log(amount, radix))

    for stage_idx in range(stages):

        stride = radix**stage_idx

        group = radix * stride

        k_base = amount // group

        stage = twiddles[stage_idx]

        for butterfly_index, butterfly in enumerate(stage):

            offset = butterfly_index % stride

            k = offset * k_base

            assert butterfly[0] == lut.twiddle_factor(0 * k, amount)
            assert butterfly[1] == lut.twiddle_factor(1 * k, amount)
            assert butterfly[2] == lut.twiddle_factor(2 * k, amount)
            assert butterfly[3] == lut.twiddle_factor(3 * k, amount)
