`include "../core/fft.sv"


//! Did not checked, Fizra started
module radix4_testbench;
  complex_t [2 : 0] twiddles;
  complex_t [3 : 0] coeffs;
  logic rounding_config;
  logic overflow_exception;
  complex_t [3 : 0] results;

  radix4 ex (
      .twiddles(twiddles),
      .coeffs(coeffs),
      .rounding_config(1'b0),
      .overflow_exception(overflow_exception),
      .result(results)
  );

  initial begin
    twiddles[0].re   = 16'h4000; // 1.0
    twiddles[0].im   = 0;        // 0.0
    twiddles[1].re   = 16'h4000; // 1.0
    twiddles[1].im   = 0;        // 0.0
    twiddles[2].re   = 0;        // 0.0
    twiddles[2].im   = 16'h4000; // 1.0
    coeffs[0].re = 16'h4000;     // 1.0
    coeffs[0].im = 16'h4000;     // 0.5
    coeffs[1].re = 16'h4000;     // 0.25
    coeffs[1].im = 16'h4000;     // 0.125
    coeffs[2].re = 16'h4000;     // 1.0
    coeffs[2].im = 16'h4000;     // 0.5
    coeffs[3].re = 16'h4000;     // 0.25
    coeffs[3].im = 16'h4000;     // 0.125

    #10;

    $display("Result[0].re = %f", results[0].re >> 14);
    $display("Result[0].im = %f", results[0].im >> 14);
    $display("Result[1].re = %f", results[1].re >> 14);
    $display("Result[1].im = %f", results[1].im >> 14);
    $display("Result[2].re = %f", results[2].re >> 14);
    $display("Result[2].im = %f", results[2].im >> 14);
    $display("Result[3].re = %f", results[3].re >> 14);
    $display("Result[3].im = %f", results[3].im >> 14);

  end

endmodule
