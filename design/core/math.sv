`ifndef MATH_SV
`define MATH_SV

typedef struct packed
{
    logic signed [15 : 0] re;
    logic signed [15 : 0] im;
} complex_t;

module truncation
#(
    parameter INPUT_WIDTH = 32,
    parameter WIDTH = 16
)
(
    input wire [INPUT_WIDTH - 1 : 0] input_value,
    output logic [WIDTH - 1 : 0] output_value
);

    assign output_value = input_value[INPUT_WIDTH - 1 : INPUT_WIDTH - WIDTH];

endmodule


`endif
