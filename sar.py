import numpy as np
import matplotlib.pyplot as plt
from sar_algo import sar_algo
from codes_to_ints import codes_to_ints
from scipy.fft import fft, fftfreq
from scipy.signal.windows import hann

# A simpler SAR ADC model 
# that runs faster by being coherent by default
# and not having intermediate time points with no action

nbits = 16
vref = 1
vdda = 1
fin = 1.03759765625e-3 # MHz
fsmp = 0.5 # MHz
ncycles = 17
nsamples = 8192
nyq = nsamples//2
runtime = ncycles/fin
dac_mis = True
dac_sigma = 0.01 #0.01 = 1% mismatch

# Sine Wave
t = np.linspace(0, runtime, nsamples)
vn1 = np.random.normal(0, 1e-4, len(t))
vin = (vdda*np.sin(2*np.pi*fin*t)*0.48)+vdda/2
vn2 = np.random.normal(1,1e-4, len(t))
vrefh = np.ones(len(t))*vref
codes = sar_algo(vin, vrefh, unit_cap=1, nbits=nbits, vaz=vdda,
                 dac_mis=dac_mis, dac_sigma=dac_sigma)
ints = codes_to_ints(codes)
vout = vref*ints/2**nbits

# fft
leak = 10
w = hann(nsamples)
vout = vout[:nsamples]
vout_norm = vout - vout.mean()
sp = fft(vout_norm*w)
sph = sp[:nyq]
mag = abs(sph)
mag_norm = (mag/(nyq))**2
#plt.stem(mag_norm)
sbin = np.argmax(mag_norm)
idxl = sbin-leak if sbin-leak >= 0 else 0
idxh = sbin+leak+1 if sbin+leak+1 <= nyq else nyq
sig_power = mag_norm[idxl:idxh].sum()
noise_power = mag_norm.sum()-sig_power
snr = 10*np.log10(sig_power/noise_power)
enob = (snr-1.76)/6.02
print(enob)
dbs = 10*np.log(mag_norm/sig_power)
plt.plot(dbs)
plt.xscale('log')
plt.grid()
plt.title('ENOB={}'.format(enob))
plt.show()


# Ramp
# Ideal ADC for transfer function
ramp = np.linspace(0,vref,nsamples)
ramp_codes_ideal = sar_algo(ramp, vref, nbits=nbits, vaz=vdda)
ramp_ints_ideal = codes_to_ints(ramp_codes_ideal)
rout_ideal = vref*ramp_ints_ideal/2**nbits
plt.plot(ramp, rout_ideal, label = 'Ideal')

# ADC Transfer Function
ramp = np.linspace(0, vref, nsamples)
ramp_codes = sar_algo(ramp, vref, nbits=nbits, vaz=vdda, dac_mis=dac_mis, dac_sigma=dac_sigma)
ramp_ints = codes_to_ints(ramp_codes)
rout = vref*ramp_ints/2**nbits
plt.plot(ramp, rout, label = 'Mismatch')
plt.legend()
plt.show()

