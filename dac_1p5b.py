from codes_to_ints import codes_to_ints

def dac_1p5b(din, vref):
    vout = codes_to_ints(din)*(vref/2)
    return vout
