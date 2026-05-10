import pytest
from fft_accelerator.address_generator import AddressGenerator

amount = [16]

addresses16 = [

    # stage0
    [
        [0,1,2,3],
        [4,5,6,7],
        [8,9,10,11],
        [12,13,14,15],
    ],

    # stage1
    [
        [0,4,8,12],
        [1,5,9,13],
        [2,6,10,14],
        [3,7,11,15],
    ]
]

@pytest.mark.parametrize("amount", amount)
def test_address_generator(amount):
    addresses = AddressGenerator.generate_addresses(amount)
    print(addresses)
    assert addresses == addresses16
