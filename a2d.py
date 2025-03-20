def a2d(voltage, vref=3, nbits=15):
    # converts analog voltage to an nbit digital code
    # between 0 and vref
    # ideal ADC
    if (type(voltage)==float or type(voltage)==int):
        if voltage > vref:
            raise ValueError('Vin > Vref')
        else:
            ncodes = 2**nbits
            code = ncodes*voltage/vref
            if (type(code) == float):
                code = int(code)
            else:
                code = code.astype(int)
    else:
        if any(v>vref for v in list(voltage)):
            raise ValueError('Vin > Vref')
        else:
            ncodes = 2**nbits
            code = ncodes*voltage/vref
            if (type(code) ==float):
                code = int(code)
            else:
                code = code.astype(int)
    return code