import numpy as np

inputFile = 'Recordings\SDRdataRaw'
output_filename = 'iq_data_int8.bin'
iq_data = np.fromfile(open(inputFile), dtype=np.float32)

int8=((iq_data/np.max(np.abs(iq_data)))*127).astype(np.int8)
int8.tofile(output_filename)
