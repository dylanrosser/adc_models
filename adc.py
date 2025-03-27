# A Python ADC library
# written by Dylan Rosser
import numpy as np
import matplotlib.pyplot as plt

class ADC:
    def __init__(self, nbits = 10, freq = 10e6, arch = 'ideal',
                 vref = 1, vdd = 1, vaz = 1, unit_cap = 100e-15,
                 dac_mis = False, dac_sigma = 0.001, noise = False,
                 vn_ref = 1e-6, vn_cmp = 1e-6, temp = 27):
        self.nbits = nbits
        self.freq = freq
        self.arch = arch
        self.vref = vref
        self.vdd = vdd
        self.vaz = vaz
        self.unit_cap = unit_cap
        self.dac_mis = dac_mis
        self.dac_sigma = dac_sigma

    def __str__(self):
        return f"{self.nbits} Bit {self.freq} SPS {self.arch} ADC"
    
    def codes_to_ints(self):
        ints = np.empty(shape=0).astype(int)
        for idx, val in enumerate(self.codes):
            i = int(val,2)
            ints=np.append(ints,i)
        return ints
    
    def convert_ideal(self, vin):
    # converts analog voltage to an nbit digital code
    # between 0 and vref
    # ideal ADC
        ncodes = 2**self.nbits
        code = ncodes*vin/self.vref
        if (type(vin)==float or type(vin)==int):
            code = int(np.clip(code, 0, ncodes-1))
        else:
            code = code.clip(0,ncodes-1).astype(int)
        return code
    
    def convert_sar(self, vin):
        # Binary Search
        cap_idx = np.append(np.flip(np.arange(0,self.nbits)),0)
        cap_vals = self.unit_cap*2**cap_idx
        cap_total = sum(cap_vals)
        cap_settings = np.zeros(shape=self.nbits+1)
        vm = self.vaz
        code = '0b'
        codes = np.empty(shape=0)
        vref_input = self.vref

        if type(vin) != np.ndarray:
            vin = np.asarray([vin])

        if type(self.vref) != np.ndarray:
            self.vref = np.ones(len(vin))*self.vref
        
        if self.dac_mis == True:
            # DAC 1-sigma is specified
            # percentage variation on decimal 0.01 = 1%
            dac_var = np.random.normal(self.unit_cap, self.unit_cap*self.dac_sigma, 
                                    len(cap_vals))
            cap_vals = dac_var*2**cap_idx

        vp = 0
        for idx, val in enumerate(vin):
            for i in range(self.nbits):
                cap_settings[i] = 1
                vp = self.vaz-val+(sum(cap_settings*cap_vals)/cap_total)*self.vref[idx]
                # compare
                if vp > vm: # if true feedback 0
                    code = code+'0'
                    cap_settings[i] = 0
                else:
                    code=code+'1'
                    cap_settings[i] = 1
            codes = np.append(codes, code)
            code = '0b'
            cap_settings = np.zeros(shape=self.nbits+1)
        self.vref = vref_input # reset to input
        return codes
    
    def convert(self, vin):
        if self.arch =='ideal':
            self.dout = self.convert_ideal(vin)
        elif self.arch == 'sar':
            self.codes = self.convert_sar(vin)
            self.dout = self.codes_to_ints()
        else: self.dout = 'arch no recognized'
        return self.dout
    
    def dac_1p5b(self, din, vref):
        vout = self.codes_to_ints(din)*(vref/2)
        return vout
    
    def dac_2b(self, din, vref):
        vout = self.codes_to_ints(din)*(vref/4)
        return vout
    
    def compare(self, vp, vm):
        if vp > vm:
            out = 1
        else: 
            out = 0
        return out
    
    def tf(self, scale=100):
        # Plot Transfer Fucntion
        # use sacle for higher resolution
        self.ramp = np.linspace(0, self.vref, 
                                scale*2**self.nbits)
        self.ramp_dout = self.convert(self.ramp)
        self.ramp_vout = self.vref*self.ramp_dout/2**self.nbits
        plt.plot(self.ramp, self.ramp_dout, 
                 label = '{}Bit {} ADC'.format(self.nbits, self.arch))
        plt.legend()
        plt.title('ADC Transfer Function')
        plt.xlabel('Input Voltage')
        plt.ylabel('Output Code')
        plt.show()
        return
