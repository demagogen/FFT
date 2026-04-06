import selector
import dual_port_ram
import fft
import address_generator
import control_block
import lut_with_twiddle_factors
import scale
import rom
import one_depth_buffer

class FFTAccelerator:
    def __init__(self):
        self.selector                 = selector.Selector()
        self.dual_port_ram            = dual_port_ram.DualPortRAM()
        self.fft                      = fft.FFT4()
        self.address_generator        = address_generator.AddressGenerator()
        self.control_block            = control_block.ControlBlock()
        self.lut_with_twiddle_factors = lut_with_twiddle_factors.LUTWithTwiddleFactors()
        self.scale                    = scale.Scale()
        self.rom                      = rom.ROM()
        self.one_depth_buffer         = one_depth_buffer.OneDepthBuffer()
