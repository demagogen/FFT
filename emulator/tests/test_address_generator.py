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


def test_address_generator64_stages():
    amount = 64
    radix = 4

    addresses = AddressGenerator.generate_addresses(amount)

    expected_stages = int(math.log(amount, radix))

    assert len(addresses) == expected_stages


def test_address_generator64_butterflies():
    amount = 64
    radix = 4

    addresses = AddressGenerator.generate_addresses(amount)

    expected = amount // radix

    for stage in addresses:
        assert len(stage) == expected

def test_address_generator64_strides():

    amount = 64
    radix = 4

    addresses = AddressGenerator.generate_addresses(amount)

    for stage_index, stage in enumerate(addresses):

        stride = radix ** stage_index

        for butterfly in stage:

            assert butterfly[1] - butterfly[0] == stride
            assert butterfly[2] - butterfly[1] == stride
            assert butterfly[3] - butterfly[2] == stride

def test_address_generator64_unique_addresses():

    amount = 64

    addresses = AddressGenerator.generate_addresses(amount)

    for stage in addresses:

        flat = []

        for butterfly in stage:
            flat.extend(butterfly)

        assert sorted(flat) == list(range(amount))

def test_address_generator256():

    amount = 256
    radix = 4

    addresses = AddressGenerator.generate_addresses(amount)

    assert len(addresses) == radix

    for stage_index, stage in enumerate(addresses):

        stride = radix ** stage_index

        assert len(stage) == 64

        flat = []

        for butterfly in stage:

            flat.extend(butterfly)

            assert butterfly[1] - butterfly[0] == stride
            assert butterfly[2] - butterfly[1] == stride
            assert butterfly[3] - butterfly[2] == stride

        assert sorted(flat) == list(range(amount))

def test_address_generator1024():

    amount = 1024
    radix = 4

    addresses = AddressGenerator.generate_addresses(amount)

    assert len(addresses) == 5

    for stage_index, stage in enumerate(addresses):

        stride = radix ** stage_index

        assert len(stage) == 256

        flat = []

        for butterfly in stage:

            flat.extend(butterfly)

            assert butterfly[1] - butterfly[0] == stride
            assert butterfly[2] - butterfly[1] == stride
            assert butterfly[3] - butterfly[2] == stride

        assert sorted(flat) == list(range(amount))
