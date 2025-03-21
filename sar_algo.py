import numpy as np

def sar_algo(vin, vref, nbits=8, vaz=3, unit_cap=100e-15, dac_mis=False, dac_sigma=0.01):
    # Fast Binary Search
    cap_idx = np.append(np.flip(np.arange(0,nbits)),0)
    cap_vals = unit_cap*2**cap_idx
    cap_total = sum(cap_vals)
    cap_settings = np.zeros(shape=nbits+1)
    vm = vaz
    code = '0b'
    codes = np.empty(shape=0)

    if type(vin) != np.ndarray:
        vin = np.asarray([vin])

    if type(vref) != np.ndarray:
        vref = np.ones(len(vin))*vref
    
    if dac_mis == True:
        # DAC 1-sigma is specified
        # percentage variation on decimal 0.01 = 1%
        dac_var = np.random.normal(unit_cap, unit_cap*dac_sigma, len(cap_vals))
        cap_vals = dac_var*2**cap_idx

    vp = 0
    for idx, val in enumerate(vin):
        for i in range(nbits):
            cap_settings[i] = 1
            vp = vaz-val+(sum(cap_settings*cap_vals)/cap_total)*vref[idx]
            # compare
            if vp > vm: # if true feedback 0
                code = code+'0'
                cap_settings[i] = 0
            else:
                code=code+'1'
                cap_settings[i] = 1
        codes = np.append(codes, code)
        code = '0b'
        cap_settings = np.zeros(shape=nbits+1)
    return codes