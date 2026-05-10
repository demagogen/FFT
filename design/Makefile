CORE_PROJECT = ../
CORE_DIR = core
TB_DIR = testbenches
BUILD_DIR = $(CORE_DIR)/build
TESTGEN_DIR = $(CORE_PROJECT)/emulator

TOP_MODULE = radix4
SOURCES = $(wildcard $(CORE_DIR)/*.sv)
TESTBENCHES = $(wildcard $(TB_DIR)/*.sv)

YOSYS = yosys
IVERILOG = iverilog
VVP = vvp

.PHONY: all synth test clean

all: synth test

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

synth: $(BUILD_DIR)
	@echo "--- Starting Synthesis ---"
	$(YOSYS) -p "read_verilog -sv $(SOURCES); hierarchy -top $(TOP_MODULE); proc; opt; fsm; opt; memory; opt; techmap; opt; write_verilog $(BUILD_DIR)/synth_output.v"
	@echo "Synthesis done. Check $(BUILD_DIR)/synth.log"

test: $(BUILD_DIR)
	@echo "--- Running Tests ---"
	$(IVERILOG) -g2012 -I core -o $(BUILD_DIR)/sim_out $(TB_DIR)/radix4_testbench.sv
	$(VVP) $(BUILD_DIR)/sim_out

clean:
	rm -rf $(BUILD_DIR)
