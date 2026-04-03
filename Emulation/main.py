# FFT (Fast Fourier Transform)
# main.py

import FFT

def main():
    for a1 in range(1, 10):
        for a2 in range(1, 10):
            for a3 in range(1, 10):
                for a4 in range(1, 10):
                    FFTclass = FFT.FFT4([a1, a2, a3, a4])
                    print("[", a1, ", ", a2, ", ", a3, ", ", a4, "]", " --- ", FFTclass.count())

main()
