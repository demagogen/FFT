module radix4
#(
    WIDTH = 16
)
(
    input logic signed [WIDTH - 1 : 0] coeff0_re,
    input logic signed [WIDTH - 1 : 0] coeff0_im,
    input logic signed [WIDTH - 1 : 0] coeff1_re,
    input logic signed [WIDTH - 1 : 0] coeff1_im,
    input logic signed [WIDTH - 1 : 0] coeff2_re,
    input logic signed [WIDTH - 1 : 0] coeff2_im,
    input logic signed [WIDTH - 1 : 0] coeff3_re,
    input logic signed [WIDTH - 1 : 0] coeff3_im,

    output logic signed [WIDTH - 1 : 0] result0_re,
    output logic signed [WIDTH - 1 : 0] result0_im,
    output logic signed [WIDTH - 1 : 0] result1_re,
    output logic signed [WIDTH - 1 : 0] result1_im,
    output logic signed [WIDTH - 1 : 0] result2_re,
    output logic signed [WIDTH - 1 : 0] result2_im,
    output logic signed [WIDTH - 1 : 0] result3_re,
    output logic signed [WIDTH - 1 : 0] result3_im
);

    assign result0_re = coeff0_re + coeff1_re + coeff2_re + coeff3_re;
    assign result0_im = coeff0_im + coeff1_im + coeff2_im + coeff3_im;
    assign result1_re = coeff0_re + coeff1_im - coeff2_re - coeff3_im;
    assign result1_im = coeff0_im - coeff1_re - coeff2_im + coeff3_re;
    assign result2_re = coeff0_re - coeff1_re + coeff2_re - coeff3_re;
    assign result2_im = coeff0_im - coeff1_im + coeff2_im - coeff3_im;
    assign result3_re = coeff0_re - coeff1_im - coeff2_re + coeff3_im;
    assign result3_im = coeff0_im + coeff1_re - coeff2_im - coeff3_im;

endmodule
