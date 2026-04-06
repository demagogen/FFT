import numpy
import FFT

def clean_complex_numpy(arr):
    return [(round(c.real, 2), round(c.imag, 2)) for c in arr]

def fft_testbench():
    print("FFT4 and numpy_fft comparison")
    for input_complex0 in range(1, 10):
        for input_complex1 in range(1, 10):
            for input_complex2 in range(1, 10):
                for input_complex3 in range(1, 10):
                    my_fft = FFT.FFT4([input_complex0, input_complex1, input_complex2, input_complex3])
                    my_fft_result = my_fft.count()
                    numpy_fft_result = numpy.fft.fft([input_complex0, input_complex1, input_complex2, input_complex3])

                    if numpy.allclose(my_fft_result, numpy_fft_result):
                        print("True: [", input_complex0, ", ", input_complex1, ", ", input_complex2, ", ", input_complex3, "] ->", my_fft_result)
                    else:
                        print("False: [", input_complex0, ", ", input_complex1, ", ", input_complex2, ", ", input_complex3, "]")
                        print("     : numpy: ", numpy_fft_result)
                        print("     : fft:   ", my_fft_result)

fft_testbench()
