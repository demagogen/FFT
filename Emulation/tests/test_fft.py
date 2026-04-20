import numpy
import pytest

from fft_accelerator.fft_accelerator import FFTAccelerator
from fixedpoint.dumps import dumps
from fixedpoint.fixedpoint import Fixedpoint
from fixedpoint.complex_fixedpoint import ComplexFixedpoint


PARAMS = {
    "with_sign": 1,
    "frac_width": 14,
    "width": 16,
    "saturate": True,
    "rounding": True,
}


# def test_fft_accelerator_int():
#     fft = FFTAccelerator()
#     for coeff0 in range(0, 10):
#         for coeff1 in range(0, 10):
#             for coeff2 in range(0, 10):
#                 for coeff3 in range(0, 10):
#                     # fixedpoint_coeffs = Fixedpoint.complex_to_verilog_bits(
#                         # [coeff0, coeff1, coeff2, coeff3]
#                     # )
#                     # fp1 = Fixedpoint(coeff0
#                     # print("fft_accelerator fp")
#                     # dumps.dumps.print_fixedpoint32_nested_bytes_list4(fixedpoint_coeffs)
#                     # fft_result = fft.driver(fixedpoint_coeffs)
#                     # fft_result_python_complex = dumps.Fixedpoint.nested_bits_to_complex(
#                         # fft_result
#                     # )
#                     expected = numpy.fft.fft([coeff0, coeff1, coeff2, coeff3])
#                     if numpy.allclose(fft_result_python_complex, expected, atol=0.1):
#                         print(
#                             "True:  ",
#                             [coeff0, coeff1, coeff2, coeff3],
#                             ", numpy: ",
#                             expected,
#                             ", fft: ",
#                             fft_result_python_complex,
#                         )
#                     else:
#                         print(
#                             "False: ",
#                             [coeff0, coeff1, coeff2, coeff3],
#                             ", numpy: ",
#                             expected,
#                             ", fft: ",
#                             fft_result_python_complex,
#                         )
#                         return
#
#
# def test_fft_accelerator_float():
#     fft = FFTAccelerator()
#     for coeff0 in numpy.arange(0.0, 1.1, 0.1):
#         for coeff1 in numpy.arange(0.0, 1.1, 0.1):
#             for coeff2 in numpy.arange(0.0, 1.1, 0.1):
#                 for coeff3 in numpy.arange(0.0, 1.1, 0.1):
#                     fixedpoint_coeffs = dumps.Fixedpoint.complex_to_verilog_bits(
#                         [coeff0, coeff1, coeff2, coeff3]
#                     )
#                     fft_result = fft.driver(fixedpoint_coeffs)
#                     fft_result_python_complex = dumps.Fixedpoint.nested_bits_to_complex(
#                         fft_result
#                     )
#                     expected = numpy.fft.fft([coeff0, coeff1, coeff2, coeff3])
#                     if numpy.allclose(fft_result_python_complex, expected, atol=0.1):
#                         print(
#                             "True: ",
#                             [coeff0, coeff1, coeff2, coeff3],
#                             ", numpy: ",
#                             expected,
#                             ", fft: ",
#                             fft_result_python_complex,
#                         )
#                     else:
#                         print(
#                             "False: ",
#                             [coeff0, coeff1, coeff2, coeff3],
#                             ", numpy: ",
#                             expected,
#                             ", fft: ",
#                             fft_result_python_complex,
#                         )
#                         return

def test_fft_accelerator():
    fft = FFTAccelerator()
    low, high = -1.5555, 1.5555
    vectors = numpy.random.uniform(low, high, size=(100, 4))

    for vector in vectors:
        inputs = [ComplexFixedpoint(v, **PARAMS) for v in vector]

        fft_result = fft.driver(inputs)

        expected = numpy.fft.fft(vector)

        actual_values = []
        for c in fft_result:
            re = c.real.raw_value / (1 << c.frac_width)
            im = c.imag.raw_value / (1 << c.frac_width)
            actual_values.append(complex(re, im))
        success = numpy.allclose(actual_values, expected, atol=0.1)

        if not success:
            print(f"\nFAIL!")
            print(f"Input:    {vector}")
            print(f"Expected: {expected}")
            print(f"Actual:   {actual_values}")
            print(f"Raw Res:  {fft_result}")
            assert False, "FFT result does not match expected numpy output"

    print(f"Successfully tested 100 vectors")


# numpy.allclose(fft_result, expected, atol=0.1)
