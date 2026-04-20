import numpy
from fixedpoint.complex_fixedpoint import ComplexFixedpoint

def test_fixed_pipeline():
    config = {"with_sign": 1, "int_width": 2, "width": 16}

    input_floats = [0.5 + 0.5j, -0.1 + 0.8j, 1.2 - 0.3j, -0.5 - 0.5j]

    fixed_objects = [ComplexFixedpoint(val, **config) for val in input_floats]
    verilog_inputs = [obj.bits for obj in fixed_objects]

    print("--- INPUT BITS ---")
    for i, bits in enumerate(verilog_inputs):
        print(f"[{i}]: {''.join(map(str, bits))}")

    obj_a = ComplexFixedpoint.from_raw_bits(verilog_inputs[0], **config)
    obj_b = ComplexFixedpoint.from_raw_bits(verilog_inputs[1], **config)

    res_fixed = obj_a + obj_b

    expected = input_floats[0] + input_floats[1]
    actual = res_fixed.to_complex()

if __name__ == "__main__":
    test_fixed_pipeline()
