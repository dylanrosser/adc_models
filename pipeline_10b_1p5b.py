import numpy as np
import matplotlib.pyplot as plt
from a2d import a2d
from codes_to_ints import codes_to_ints
from scipy.fft import fft, fftfreq
from scipy.signal.windows import blackman
from compare import compare
from dac_1p5b import dac_1p5b
from dac_2b import dac_2b
from error_amp import error_amp
from flash_1p5b import flash_1p5b
from flash_2b import flash_2b

# 10B Pipeline
# 1.5B per state with 0.5B interstage redundancy

nbits = 10
vref = 1.5
vdda = 1.5
fin = 1.03759765625 # MHz
fsmp = 0.5
ncycles = 17
nsamples = 8192
nyq = nsamples//2
runtime = ncycles/fin

t = np.linspace(0, runtime, nsamples)
vin = (vdda*np.sin(2*np.pi*fin*t)*0.495)+vdda/2

# stage 1
ds1 = flash_1p5b(vin,vref)
vdac1 = dac_2b(ds1, vref)
er1 = error_amp(vin, vdac1, 2)
# stage 2
ds2 = flash_1p5b(er1,vref)
vdac2 = dac_2b(ds2, vref)
er2 = error_amp(er1, vdac2, 2)
# stage 3
ds3 = flash_1p5b(er2,vref)
vdac3 = dac_2b(ds3, vref)
er3 = error_amp(er2, vdac3, 2)
# stage 4
ds4 = flash_1p5b(er3,vref)
vdac4 = dac_2b(ds4, vref)
er4 = error_amp(er3, vdac4, 2)
# stage 5
ds5 = flash_1p5b(er4,vref)
vdac5 = dac_2b(ds5, vref)
er5 = error_amp(er4, vdac5, 2)
# stage 6
ds6 = flash_1p5b(er5,vref)
vdac6 = dac_2b(ds6, vref)
er6 = error_amp(er5, vdac6, 2)
# stage 7
ds7 = flash_1p5b(er6,vref)
vdac7 = dac_2b(ds7, vref)
er7 = error_amp(er6, vdac7, 2)
# stage 8
ds8 = flash_1p5b(er7,vref)
vdac8 = dac_2b(ds8, vref)
er8 = error_amp(er7, vdac8, 2)
# stage 9
ds9 = flash_2b(er8,vref)

is1 = codes_to_ints(ds1)
is2 = codes_to_ints(ds2)
is3 = codes_to_ints(ds3)
is4 = codes_to_ints(ds4)
is5 = codes_to_ints(ds5)
is6 = codes_to_ints(ds6)
is7 = codes_to_ints(ds7)
is8 = codes_to_ints(ds8)
is9 = codes_to_ints(ds9)

results = np.array([is1, is2, is3, is4, is5, is6, is7, is8, is9])

# combine bits
# Andrew Abo pg 88
dout = []
for idx, val in enumerate(is1):
    d = 0
    for i in range(9):
        d = d+ results[i][idx]*2**(9-(i+1)) # (9+1-i-1??)
    dout.append(d)

dout = np.asarray(dout)

# PLOTS

fig, axs = plt.subplots(2,1,sharex=True)
axs[0].plot(vin)
axs[0].set_title('Vin (V)')
axs[1].plot(dout)
axs[1].set_title('Dout')

#fft
leak = 20
dout_norm = dout - dout.mean()
w = blackman(nsamples)
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

plt.clf()
plt.stem(mag_norm)
plt.title('FFT: ENOB = {}'.format(enob))
plt.show()

