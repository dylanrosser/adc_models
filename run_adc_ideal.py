import numpy as np
import matplotlib.pyplot as plt
from a2d import a2d
from scipy.fft import fft, fftfreq
from scipy.signal.windows import blackman

nbits = 10
vref = 1.5
vdda = 1.5
fin = 1.03759765625 # MHz
fsmp = 0.5
ncycles = 17
nsamples = 8192
nyq = nsamples//2
runtime = ncycles/fin
leak = 20
w = blackman(nsamples)

t = np.linspace(0, runtime, nsamples)
vin = (vdda*np.sin(2*np.pi*fin*t)*0.495)+vdda/2
vin_norm = vin-vin.mean()

# fft on imput
sp = fft(vin_norm*w)
sph = sp[:nyq]
mag = abs(sph)
mag_norm = (mag/(nyq))**2
sbin = np.argmax(mag_norm)
idxl = sbin-leak if sbin-leak >=0 else 0
idxh = sbin+leak+1 if sbin+leak+1 <= nyq else nyq
sig_power = mag_norm[idxl:idxh].sum()
noise_power = mag_norm.sum()-sig_power
snr = 10*np.log10(sig_power/noise_power)
enob = (snr-1.76)/6.02
print('ENOB = ', enob)

#fft on output
dout = a2d(vin, vref=vref, nbits=nbits)
vout = vref*dout/(2**nbits)
dout_norm = dout - dout.mean()
vout_norm = vout - vout.mean()
sp = fft(dout_norm*w)
sph = sp[:nyq]
mag = abs(sph)
mag_norm = (mag/(nyq))**2
sbin = np.argmax(mag_norm)
idxl = sbin-leak if sbin-leak >=0 else 0
idxh = sbin+leak+1 if sbin+leak+1 <= nyq else nyq
sig_power = mag_norm[idxl:idxh].sum()
noise_power = mag_norm.sum()-sig_power
snr = 10*np.log10(sig_power/noise_power)
enob = (snr-1.76)/6.02
print('ENOB = ', enob)