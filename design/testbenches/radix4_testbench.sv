`include "fft.sv"

module radix4_testbench();

    localparam WIDTH = 16;

    logic signed [WIDTH - 1 : 0] coeff0_re;
    logic signed [WIDTH - 1 : 0] coeff0_im;
    logic signed [WIDTH - 1 : 0] coeff1_re;
    logic signed [WIDTH - 1 : 0] coeff1_im;
    logic signed [WIDTH - 1 : 0] coeff2_re;
    logic signed [WIDTH - 1 : 0] coeff2_im;
    logic signed [WIDTH - 1 : 0] coeff3_re;
    logic signed [WIDTH - 1 : 0] coeff3_im;

    logic signed [WIDTH - 1 : 0] result0_re;
    logic signed [WIDTH - 1 : 0] result0_im;
    logic signed [WIDTH - 1 : 0] result1_re;
    logic signed [WIDTH - 1 : 0] result1_im;
    logic signed [WIDTH - 1 : 0] result2_re;
    logic signed [WIDTH - 1 : 0] result2_im;
    logic signed [WIDTH - 1 : 0] result3_re;
    logic signed [WIDTH - 1 : 0] result3_im;

    radix4 dut(
        .coeff0_re(coeff0_re),
        .coeff0_im(coeff0_im),
        .coeff1_re(coeff1_re),
        .coeff1_im(coeff1_im),
        .coeff2_re(coeff2_re),
        .coeff2_im(coeff2_im),
        .coeff3_re(coeff3_re),
        .coeff3_im(coeff3_im),

        .result0_re(result0_re),
        .result0_im(result0_im),
        .result1_re(result1_re),
        .result1_im(result1_im),
        .result2_re(result2_re),
        .result2_im(result2_im),
        .result3_re(result3_re),
        .result3_im(result3_im)
    );

    initial begin
        coeff0_re = 16'h4000;
        coeff0_im = 16'h0;
        coeff1_re = 16'h0;
        coeff1_im = 16'h0;
        coeff2_re = 16'h0;
        coeff2_im = 16'h0;
        coeff3_re = 16'h0;
        coeff3_im = 16'h0;
        #100;
        $display("result0_re = %h", result0_re);
        $display("result0_im = %h", result0_im);
        $display("result1_re = %h", result1_re);
        $display("result1_im = %h", result1_im);
        $display("result2_re = %h", result2_re);
        $display("result2_im = %h", result2_im);
        $display("result3_re = %h", result3_re);
        $display("result3_im = %h", result3_im);
    end

endmodule
