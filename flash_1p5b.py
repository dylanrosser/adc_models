import numpy as np
from compare import compare

def flash_1p5b(vin, vref):
    dout = []
    for idx, val in enumerate(vin):
        c0 = compare(vin[idx], 3*vref/8)
        c1 = compare(vin[idx], 5*vref/8)
        if not c0:
            d = '0b00'
        elif not c1:
            d = '0b01'
        else:
            d = '0b10'
        dout.append(d)
    return np.asarray(dout)