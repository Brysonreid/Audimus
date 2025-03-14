import SoapySDR

sdr = SoapySDR.Device()

temperature = sdr.getSensor("temp")
print(temperature)
