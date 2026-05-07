`include "../core/fft.sv"

module radix2_testbench;
  localparam int TESTS_AMOUNT = 200;
  localparam int TEST_SIZE = 128;
  localparam int TESTS_BITS   = TESTS_AMOUNT * TEST_SIZE;
  localparam int VALUE_SIZE = 16;
  logic [TEST_SIZE - 1 : 0] tests [TESTS_AMOUNT - 1 : 0];
  logic [TEST_SIZE - 1 : 0] answers [TESTS_AMOUNT - 1 : 0];
  complex_t [1 : 0] expected_answer;

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
    logic [VALUE_SIZE - 1 : 0] first_digit;
    $readmemb("tests/radix2_inputs.txt", tests);
    $readmemb("tests/radix2_answers.txt", answers);
    first_digit = tests[0][VALUE_SIZE - 1 : 0];
    if (first_digit == 1'hxxxx) begin
      $display("Tests were not read");
      $finish;
    end
    if (read_answers_ret_value == 1) begin
      $display("Answers were not read");
      $finish;
    end

    twiddle.re = 16'h4000;
    twiddle.im = 16'h0000;

    for (int test = TESTS_AMOUNT - 1; test >= 0; test--) begin
      coeffs[0].re = tests[test][VALUE_SIZE - 1 : 0];
      coeffs[0].im = tests[test][2 * VALUE_SIZE - 1 : VALUE_SIZE];
      coeffs[1].re = tests[test][3 * VALUE_SIZE - 1 : 2 * VALUE_SIZE];
      coeffs[1].im = tests[test][4 * VALUE_SIZE - 1 : 3 * VALUE_SIZE];

      #10;
      expected_answer[0].re = answers[test][VALUE_SIZE - 1 : 0];
      expected_answer[0].im = answers[test][2 * VALUE_SIZE - 1 : VALUE_SIZE];
      expected_answer[1].re = answers[test][3 * VALUE_SIZE - 1 : 2 * VALUE_SIZE];
      expected_answer[1].im = answers[test][4 * VALUE_SIZE - 1 : 3 * VALUE_SIZE];

      #10;

      if (coeffs[0].re == expected_answer[0].re &&
          coeffs[0].im == expected_answer[0].im &&
          coeffs[1].re == expected_answer[1].re &&
          coeffs[1].im == expected_answer[1].im)
          begin
            $display("Test #%d: SUCCESS", test);
          end
      else begin
        $display("Test #%d: FAILURE: answers: %h %h %h %h: expected: %h %h %h %h",
          test, coeffs[0].re, coeffs[0].im, coeffs[1].re, coeffs[1].im,
          expected_answer[0].re, expected_answer[0].im, expected_answer[1].re, expected_answer[1].im);
      end

      #10;
    end
    // twiddle.re   = 16'h4000;  // 1.0
    // twiddle.im   = 16'h0000;  // 0.0
    // coeffs[0].re = 16'h4000;  // 1.0
    // coeffs[0].im = 16'h4000;  // 1.0
    // coeffs[1].re = 16'h4000;  // 1.0
    // coeffs[1].im = 16'h4000;  // 1.0
    // #10;

    // $display("Result[0].re = %f", results[0].re >> 14);
    // $display("Result[0].im = %f", results[0].im >> 14);
    // $display("Result[1].re = %f", results[1].re >> 14);
    // $display("Result[1].im = %f", results[1].im >> 14);

  end

endmodule
