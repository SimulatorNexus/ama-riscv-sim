import random
import argparse
import numpy as np

# format numpy array as C array
def np2C(var, arr, dir="in"):
    return f"NF_{dir.upper()} " + var + f"[ARR_LEN]" + \
            " = {" + ", ".join([f"{x}" for x in arr]) + "};"

def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b

ops = [add, sub, mul, div]
ops_n = [op.__name__ for op in ops]
ops_sign = ["+", "-", "*", "/"]

ARR_LEN = 32
num = {
    "uint8_t": {"nf_in": np.uint8, "nf_out": np.uint32},
    "int8_t": {"nf_in": np.int8, "nf_out": np.int32},
    "uint16_t": {"nf_in": np.uint16, "nf_out": np.uint32},
    "int16_t": {"nf_in": np.int16, "nf_out": np.int32},
    "uint32_t": {"off_add": 2, "off_sub": 2, "off_mul": 16,
                 "nf_in": np.uint32, "nf_out": np.uint32},
    "int32_t": {"off_add": 2, "off_sub": 2, "off_mul": 16,
                "nf_in": np.int32, "nf_out": np.int32},
    "uint64_t": {"off_add": 2, "off_sub": 3, "off_mul": 34, "off_div": 2,
                 "nf_in": np.uint64, "nf_out": np.uint64},
    "int64_t": {"off_add": 2, "off_sub": 3, "off_mul": 34, "off_div": 2,
                "nf_in": np.int64, "nf_out": np.int64},
    #"half": {"min": -1, "max": 1, "nf_in": np.float16, "nf_out": np.float32},
    "float": {"min": -1, "max": 1, "nf_in": np.float32, "nf_out": np.float32},
    "double": {"min": -1, "max": 1, "nf_in": np.float64, "nf_out": np.float64},
}

fp_c_map = {np.float16: "_Float16", np.float32: "float", np.float64: "double"}

def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate code for the vector test and specified operation')
    parser.add_argument(
        '--op', required=True, type=str, choices=ops_n, help='Operation type')
    return parser.parse_args()

args = parse_args()
OUT = f"test_arrays_{args.op}.h"

# find the operation
op, idx = [zop for zop in zip(ops, range(len(ops))) 
           if zop[0].__name__ == args.op][0]

code = []
code.append("#include <stdint.h>\n")
code.append("#define ARR_LEN 32\n")
code.append("#define OP " + ops_sign[idx] + "\n")

random.seed(0)
for key,value in num.items():
    def_check = "#if " if key == "uint8_t" else "#elif "
    code.append(def_check + "defined(NF_" + \
                value["nf_in"].__name__.upper() + ")")

    if "float" in value["nf_in"].__name__:
        typ_min = value["min"]
        typ_max = value["max"]
        ctypes = [fp_c_map[value["nf_in"]], fp_c_map[value["nf_out"]]]
    else:
        shift_amount = value.get(f"off_{op.__name__}", 0)
        typ_min = np.iinfo(value["nf_in"]).min >> shift_amount
        typ_max = np.iinfo(value["nf_in"]).max >> shift_amount
        ctypes = [value["nf_in"].__name__ + "_t",
                  value["nf_out"].__name__ + "_t"]
    
    code.append("#define NF_IN " + ctypes[0])
    code.append("#define NF_OUT " + ctypes[1])
    
    value['a'] = (np.array([random.uniform(typ_min,typ_max) 
                            for _ in range(ARR_LEN)], dtype=value["nf_in"]))
    value['b'] = (np.array([random.uniform(typ_min,typ_max) 
                            for _ in range(ARR_LEN)], dtype=value["nf_in"]))
    
    # bias for unsigned int subtraction
    if "uint" in key and op.__name__ == "sub":
        value['b'] = value['b'] >> (4 + ("32" in key)*2 + ("64" in key)*8)
    
    # bias for int division
    if "int" in key and op.__name__ == "div":
        value['b'] = value['b'] >> (4 + ("32" in key)*2 + ("64" in key)*6)
        # ensure no zeros in the denominator
        value['b'] = np.where(value['b'] == 0, 13, value['b'])
    
    # ensure no zeros in the denominator for float division
    if "float" in key and op.__name__ == "div":
        value['b'] = np.where(value['b'] == 0, 0.01, value['b'])
    
    # cast all to nf_out
    value['a'] = value['a'].astype(value["nf_out"])
    value['b'] = value['b'].astype(value["nf_out"])
    value['ref'] = np.zeros(ARR_LEN, dtype=value["nf_out"])
    
    # calculate the result
    for i in range(ARR_LEN):
        value['ref'][i] = op(value['a'][i], value['b'][i])
    
    code.append(np2C('a', value['a'], "in"))
    code.append(np2C('b', value['b'], "in"))
    code.append(np2C('c', [0], "out"))
    code.append(np2C('ref', value['ref'], "out") + "\n")

code.append('#else')
code.append('_Static_assert(0, "NF not defined");')
code.append('#endif\n')

with open(OUT, "w") as f:
    f.write("\n".join(code))
    print(f"Generated {OUT}")
