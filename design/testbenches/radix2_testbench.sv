`include "../core/fft.sv"

module radix2_testbench;
  complex_t twiddle;
  complex_t [1 : 0] coeffs;
  logic rounding_config;
  logic overflow_exception;
  complex_t [1 : 0] results;

  radix2 ex (
      .twiddle(twiddle),
      .coeffs(coeffs),
      .rounding_config(0),
      .overflow_exception(overflow_exception),
      .result(results)
  );

  initial begin
    twiddle.re   = 16'h4000;  // 1.0
    twiddle.im   = 0;
    coeffs[0].re = 16'h4000;  // 1.0
    coeffs[0].im = 16'h2000;  // 0.5
    coeffs[1].re = 16'h1000;  // 0.25
    coeffs[1].im = 16'h0800;  // 0.125
    #10;

    $display("Result[0].re = %f", results[0].re / 16384.0);
    $display("Result[0].im = %f", results[0].im / 16384.0);

  end

endmodule
