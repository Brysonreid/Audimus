import numpy as np

output_filename = 'iq_data_int8.bin'

iq_data2 = np.fromfile(open(output_filename), dtype=np.int8)
float32=iq_data2.astype(np.int16)
float32.tofile(output_filename)