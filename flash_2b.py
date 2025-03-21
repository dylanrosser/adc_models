import numpy as np
from compare import compare

def flash_2b(vin, vref):
    dout = []
    for idx, val in enumerate(vin):
        c0 = compare(vin[idx], vref/4)
        c1 = compare(vin[idx], vref/2)
        c2 = compare(vin[idx], 3*vref/4)
        if not c0:
            d = '0b00'
        elif not c1:
            d = '0b01'
        elif not c2:
            d = '0b10'
        else:
            d = '0b11'
        dout.append(d)
    return np.asarray(dout)
