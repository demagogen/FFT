import numpy as np
import FFT

coeffs = [5, 1, 2, 3]

fft_result = np.fft.fft(coeffs)

def fft_testbench():
    print("FFT4 and numpy_fft comparison")
    for a1 in range(1, 10):
        for a2 in range(1, 10):
            for a3 in range(1, 10):
                for a4 in range(1, 10):
                    my_FFT = FFT.FFT4([a1, a2, a3, a4])
                    my_FFT_result = my_FFT.count()
                    numpy_fft_result = np.fft.fft([a1, a2, a3, a4])
                    if np.array_equal(my_FFT_result, numpy_fft_result):
                        print("True: a0 = ", a1, " a1 = ", a2, " a2 = ", a3, " a3 = ", a4)
                    else:
                        print("False: a0 = ", a1, " a1 = ", a2, " a2 = ", a3, " a3 = ", a4)
                        print("     : numpy: ", numpy_fft_result)
                        print("     : fft:   ", my_FFT_result)

print(fft_result)
fft_testbench()
