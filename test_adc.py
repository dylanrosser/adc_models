import adc
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal.windows import blackman

ideal_adc = adc.ADC()
adc2b = adc.ADC(nbits=2)
sar_adc = adc.ADC(arch = 'sar')

nbits = 10
vref = 1
vdda = 1
fin = 1.03759765625 # MHz
ncycles = 17
nsamples = 8192
nyq = nsamples//2
runtime = ncycles/fin
leak = 20
w = blackman(nsamples)

t = np.linspace(0, runtime, nsamples)
vin = (vdda*np.sin(2*np.pi*fin*t)*0.495)+vdda/2
vin_norm = vin-vin.mean()

dout1 = ideal_adc.convert(vin)
dout2 = sar_adc.convert(vin)

# plot transfer functions
adc2b.tf()
ideal_adc.tf()
sar_adc.tf()

# A 6 Bit SAR ADC with 1% DAC Mismatch
sar_adc2 = adc.ADC(arch = 'sar', nbits = 6,
                    dac_mis=True, dac_sigma=0.01)

