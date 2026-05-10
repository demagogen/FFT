`include "math.sv"

module radix4
(
    input wire complex_t [2 : 0] twiddles,
    input wire complex_t [3 : 0] coeffs,
    input wire rounding_config,
    output logic overflow_exception,
    output complex_t [3 : 0] result
);



endmodule
