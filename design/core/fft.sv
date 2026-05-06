typedef struct packed
{
    logic signed [15 : 0] re;
    logic signed [15 : 0] im;
} complex_t;

// module trunctation

module radix2
(
    input wire complex_t twiddle,
    input wire complex_t [1 : 0] coeffs,
    input wire rounding_config,
    output logic overflow_exception,
    output complex_t [1 : 0] result
);

    logic signed [31 : 0] tmp_re;
    logic signed [31 : 0] tmp_im;

    assign tmp_re = (twiddle.re * coeffs[1].re - twiddle.im * coeffs[1].im);
    assign tmp_im = (twiddle.re * coeffs[1].im + twiddle.im * coeffs[1].re);

    assign result[0].re = coeffs[0].re + tmp_re[15 : 0];
    assign result[0].im = coeffs[0].im + tmp_im[15 : 0];
    assign result[1].re = coeffs[0].re - tmp_re[15 : 0];
    assign result[1].im = coeffs[0].im - tmp_im[15 : 0];

endmodule
