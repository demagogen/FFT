import pytest
import math
from fft_accelerator.address_generator import AddressGenerator


def test_address_generator4():

    expected = [
        [
            [0, 1, 2, 3],
        ]
    ]

    actual = AddressGenerator.generate_addresses(4)

    assert actual == expected


def test_address_generator16():
    addresses16 = [
        [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15],
        ],
        [
            [0, 4, 8, 12],
            [1, 5, 9, 13],
            [2, 6, 10, 14],
            [3, 7, 11, 15],
        ],
    ]

    addresses = AddressGenerator.generate_addresses(16)
    assert addresses == addresses16


def test_fft64_stage_count():
    addresses = AddressGenerator.generate_addresses(64)

    expected_stages = int(math.log(64, 4))

    assert len(addresses) == expected_stages


def test_fft64_butterflies_per_stage():

    addresses = AddressGenerator.generate_addresses(64)

    expected = 64 // 4

    for stage in addresses:
        assert len(stage) == expected

def test_fft64_stride():

    N = 64

    addresses = AddressGenerator.generate_addresses(N)

    for stage_idx, stage in enumerate(addresses):

        stride = 4 ** stage_idx

        for butterfly in stage:

            assert butterfly[1] - butterfly[0] == stride
            assert butterfly[2] - butterfly[1] == stride
            assert butterfly[3] - butterfly[2] == stride
