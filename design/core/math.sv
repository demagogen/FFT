`ifndef MATH_SV
`define MATH_SV

typedef struct packed {
  logic signed [15 : 0] re;
  logic signed [15 : 0] im;
} complex_t;

module truncation #(
    parameter INPUT_WIDTH = 32,
    parameter WIDTH = 16
) (
    input wire [INPUT_WIDTH - 1 : 0] input_value,
    output logic [WIDTH - 1 : 0] output_value
);

  assign output_value = input_value[INPUT_WIDTH-1 : INPUT_WIDTH-WIDTH];

endmodule

module rounding_to_nearest #(
    parameter INPUT_WIDTH = 32,
    parameter WIDTH = 16
) (
    input wire [INPUT_WIDTH - 1 : 0] input_value,
    output logic [WIDTH - 1 : 0] output_value
);

  localparam SHIFT = INPUT_WIDTH - WIDTH;

  logic [WIDTH : 0] tmp_rounded;

  assign tmp_rounded  = input_value + (1'b1 << (SHIFT - 1));
  assign output_value = tmp_rounded[INPUT_WIDTH-1 : SHIFT];
endmodule

module convergent_rounding #(
    parameter INPUT_WIDTH = 32,
    parameter WIDTH = 16
) (
    input wire [INPUT_WIDTH - 1 : 0] input_value,
    output logic [WIDTH - 1 : 0] output_value
);

  localparam SHIFT = INPUT_WIDTH - WIDTH;

  wire  [WIDTH - 1:0] truncated = input_value[INPUT_WIDTH-1 : SHIFT];
  wire                half_bit = input_value[SHIFT-1];
  wire                lower_bits = input_value[SHIFT-2 : 0];
  wire                is_even = ~truncated[0];

  logic               plus_one;
  always_comb begin
    if (half_bit) begin
      if (lower_bits) plus_one = 1;
      else plus_one = ~is_even;
    end else begin
      plus_one = 0;
    end
  end

  assign output_value = truncated + plus_one;
endmodule

`endif
