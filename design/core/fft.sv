module buffer4
#(
    parameter WIDTH = 16,
    parameter FRAC_WIDTH = 15
)
(
    input clk,
    input write_en,
    input [WIDTH - 1 : 0] write_data,
    input read_ready,
    output [WIDTH - 1 : 0] read_data,
    output read_valid
);

    typedef enum logic [2 : 0]
    {
        IDLE,
        READ,
        PROCESS,
        DONE,
        ERROR
    } state_t;

    state_t current_state;
    state_t next_state;
    logic [1 : 0] counter;

    always_comb begin
        case (current_state)
            IDLE: if (write_en) next_state = READ;
            READ: if (write_en) next_state = PROCESS;
            PROCESS:
                begin
                    if (counter < 2'd3 && write_en)
                        next_state = IDLE;
                    else if (counter == 2'd3 && write_en)
                        next_state = DONE;
                    else
                        next_state = ERROR;
                end
            ERROR: next_state = IDLE;
            DONE: if (write_en) next_state = IDLE;
        endcase
    end

endmodule
