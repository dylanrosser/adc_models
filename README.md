# adc_models
Open Source Data Converter Models written in python

# SAR ADC Model
This SAR ADC is modeled in python. It is high parameterizable, including the resolution and sample rate. It uses bottom plate sampling 
and a binary weighted CDAC. It has the capability to include DAC mismatch effects or random noise, to view the effects on SNDR or the transfer function.

See test_adc.py for examples on how to use this library.

# Create a 10bit ideal ADC and display it's transfer function:
```
import adc
ideal_adc = adc.ADC()
ideal_adc.tf()
```
# Create an ideal 2bit ADC and display its transfer function:
```
import adc
adc2b = adc.ADC(nbits=2)
adc2b.tf()
```
# A 6 Bit SAR ADC with 1% DAC Mismatch
```
import adc
sar_adc2 = adc.ADC(arch = 'sar', nbits = 6,
                    dac_mis=True, dac_sigma=0.01)
sar_adc2.tf()
```
# ENOB and FFT
I want to write methods so that you can just do
adc.fft() or adc.enob to get these things 
(INL/DNL/SQNR/SNDR/SFDR/TUE/gain and offset errors as well) 

For now you can get an fft and an enob by following sar.py

You can also build a custom SAR by modifying sar.py to your desired configuration, then running:
> python sar.py

# Pipline ADC Model
This is a 10b pipeline ADC with 0.5b interstage redundancy modeled in python.

Example usage
> python pipeline_10b_1p5b.py
