`include "math.sv"

module radix2 (
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

    logic signed [15 : 0] tmp_re_rounded, tmp_im_rounded;
    convergent_rounding tmp_rer(.input_value(tmp_re), .output_value(tmp_re_rounded));
    convergent_rounding tmp_imr(.input_value(tmp_im), .output_value(tmp_im_rounded));

  assign result[0].re = coeffs[0].re + tmp_re_rounded;
  assign result[0].im = coeffs[0].im + tmp_im_rounded;
  assign result[1].re = coeffs[0].re - tmp_re_rounded;
  assign result[1].im = coeffs[0].im - tmp_im_rounded;

endmodule


module radix4
(
    input wire complex_t [2 : 0] twiddles,
    input wire complex_t [3 : 0] coeffs,
    input wire rounding_config,
    output logic overflow_exception,
    output complex_t [3 : 0] result
);

    complex_t [1 : 0] tmp_result0, tmp_result1;
    logic overflow_exception0, overflow_exception1;

    radix2 tmp0(
        .twiddle(twiddles[0]),
        .coeffs({coeffs[2], coeffs[0]}),
        .rounding_config(rounding_config),
        .overflow_exception(overflow_exception0),
        .result(tmp_result0)
    );

    radix2 tmp1(
        .twiddle(twiddles[0]),
        .coeffs({coeffs[3], coeffs[1]}),
        .rounding_config(rounding_config),
        .overflow_exception(overflow_exception1),
        .result(tmp_result1)
    );

    logic signed [31 : 0] tmp0_re, tmp1_re;
    logic signed [31 : 0] tmp0_im, tmp1_im;

    assign tmp0_re = (twiddles[1].re * tmp_result1[0].re - twiddles[1].im * tmp_result1[0].im);
    assign tmp0_im = (twiddles[1].re * tmp_result1[0].im + twiddles[1].im * tmp_result1[0].re);
    assign tmp1_re = (twiddles[2].re * tmp_result1[1].re - twiddles[2].im * tmp_result1[1].im);
    assign tmp1_im = (twiddles[2].re * tmp_result1[1].im + twiddles[2].im * tmp_result1[1].re);

    logic signed [15 : 0] tmp0_re_rounded, tmp1_re_rounded, tmp0_im_rounded, tmp1_im_rounded;

    convergent_rounding rounding0_re (.input_value(tmp0_re), .output_value(tmp0_re_rounded));
    convergent_rounding rounding0_im (.input_value(tmp0_im), .output_value(tmp0_im_rounded));
    convergent_rounding rounding1_re (.input_value(tmp1_re), .output_value(tmp1_re_rounded));
    convergent_rounding rounding1_im (.input_value(tmp1_im), .output_value(tmp1_im_rounded));

    assign result[0].re = tmp_result0[0].re + tmp0_re_rounded;
    assign result[0].im = tmp_result0[0].im + tmp0_im_rounded;
    assign result[1].re = tmp_result0[1].re + tmp1_re_rounded;
    assign result[1].im = tmp_result0[1].im + tmp1_im_rounded;
    assign result[2].re = tmp_result0[0].re - tmp0_re_rounded;
    assign result[2].im = tmp_result0[0].im - tmp0_im_rounded;
    assign result[3].re = tmp_result0[1].re - tmp1_re_rounded;
    assign result[3].im = tmp_result0[1].im - tmp1_im_rounded;

    assign overflow_exception = overflow_exception0 | overflow_exception1;
endmodule
