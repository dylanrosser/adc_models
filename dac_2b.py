from codes_to_ints import codes_to_ints

def dac_2b(din, vref):
    vout = codes_to_ints(din)*(vref/4)
    return vout
