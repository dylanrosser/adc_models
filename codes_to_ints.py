import numpy as np

def codes_to_ints(codes):
    ints = np.empty(shape=0)
    for idx, val in enumerate(codes):
        i = int(val,2)
        ints=np.append(ints,i)
    return ints