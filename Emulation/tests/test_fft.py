import numpy
import pytest

from fft_accelerator.fft_accelerator import FFTAccelerator
from fixedpoint.dumps import dumps
from fixedpoint.fixedpoint import Fixedpoint


def test_fft_accelerator_int():
    fft = FFTAccelerator()
    for coeff0 in range(0, 10):
        for coeff1 in range(0, 10):
            for coeff2 in range(0, 10):
                for coeff3 in range(0, 10):
                    fixedpoint_coeffs = dumps.Fixedpoint.complex_to_verilog_bits(
                        [coeff0, coeff1, coeff2, coeff3]
                    )
                    print("fft_accelerator fp")
                    dumps.dumps.print_fixedpoint32_nested_bytes_list4(fixedpoint_coeffs)
                    fft_result = fft.driver(fixedpoint_coeffs)
                    fft_result_python_complex = dumps.Fixedpoint.nested_bits_to_complex(
                        fft_result
                    )
                    expected = numpy.fft.fft([coeff0, coeff1, coeff2, coeff3])
                    if numpy.allclose(fft_result_python_complex, expected, atol=0.1):
                        print(
                            "True:  ",
                            [coeff0, coeff1, coeff2, coeff3],
                            ", numpy: ",
                            expected,
                            ", fft: ",
                            fft_result_python_complex,
                        )
                    else:
                        print(
                            "False: ",
                            [coeff0, coeff1, coeff2, coeff3],
                            ", numpy: ",
                            expected,
                            ", fft: ",
                            fft_result_python_complex,
                        )
                        return


def test_fft_accelerator_float():
    fft = FFTAccelerator()
    for coeff0 in numpy.arange(0.0, 1.1, 0.1):
        for coeff1 in numpy.arange(0.0, 1.1, 0.1):
            for coeff2 in numpy.arange(0.0, 1.1, 0.1):
                for coeff3 in numpy.arange(0.0, 1.1, 0.1):
                    fixedpoint_coeffs = dumps.Fixedpoint.complex_to_verilog_bits(
                        [coeff0, coeff1, coeff2, coeff3]
                    )
                    fft_result = fft.driver(fixedpoint_coeffs)
                    fft_result_python_complex = dumps.Fixedpoint.nested_bits_to_complex(
                        fft_result
                    )
                    expected = numpy.fft.fft([coeff0, coeff1, coeff2, coeff3])
                    if numpy.allclose(fft_result_python_complex, expected, atol=0.1):
                        print(
                            "True: ",
                            [coeff0, coeff1, coeff2, coeff3],
                            ", numpy: ",
                            expected,
                            ", fft: ",
                            fft_result_python_complex,
                        )
                    else:
                        print(
                            "False: ",
                            [coeff0, coeff1, coeff2, coeff3],
                            ", numpy: ",
                            expected,
                            ", fft: ",
                            fft_result_python_complex,
                        )
                        return
