import numpy as np

output_filename = 'Pi/Recordings/SDRdata2025-04-02-16_18_321'

iq_data2 = np.fromfile(open(output_filename), dtype=np.int8)
float32=iq_data2.astype(np.int16)
float32.tofile(output_filename)