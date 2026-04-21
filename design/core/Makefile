CORE_DIR = core
TB_DIR = testbenches
BUILD_DIR = $(CORE_DIR)/build

TOP_MODULE = top
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
	$(YOSYS) -p "read_sv $(SOURCES); hierarchy -top $(TOP_MODULE); proc; opt; fsm; opt; memory; opt; techmap; opt; write_verilog $(BUILD_DIR)/synth_output.v" > $(BUILD_DIR)/synth.log 2>&1
	@echo "Synthesis done. Check $(BUILD_DIR)/synth.log"

test: $(BUILD_DIR)
	@echo "--- Running Tests ---"
	$(IVERILOG) -g2012 -I $(CORE_DIR) -o $(BUILD_DIR)/sim_out $(SOURCES) $(TESTBENCHES) > $(BUILD_DIR)/compile_sim.log 2>&1
	$(VVP) $(BUILD_DIR)/sim_out > $(BUILD_DIR)/test_results.log
	@echo "Tests finished. Results in $(BUILD_DIR)/test_results.log"

clean:
	rm -rf $(BUILD_DIR)
