# adc_models
Open Source Data Converter Models written in python

# SAR ADC Model
This SAR ADC is modeled in python. It is high parameterizable, including the resolution and sample rate. It uses bottom plate sampling 
and a binary weighted CDAC. It has the capability to include DAC mismatch effects or random noise, to view the effects on SNDR or the transfer function.

Example usage currently involves modifying sar.py to your desired configuration, then running:
> python sar.py

In the future I hope to turn this into a class, so usage will be a little different

# Pipline ADC Model
This is a 10b pipeline ADC with 0.5b interstage redundancy modeled in python.

Example usage
> python pipeline_10b_1p5b.py
