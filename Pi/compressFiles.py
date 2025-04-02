import numpy as np

inputFile = 'Recordings/SDRdata2025-04-02-15_06_03'
output_filename = 'Recordings/SDRdata2025-04-02-15_06_03_compress'

#we want to bring in 24 M bytes of data, dtype is float32 (32bits = 4 byts) = 6M float values loaded in per loop
#meaning 3M samples (complex64)

Offset = 24000000
with open(output_filename,"w") as f:
    
    for I in range(19):
        print(I)
        iq_data = np.fromfile(open(inputFile), dtype=np.float32,count = int(Offset/4),offset = Offset*I)
        print(len(iq_data))
        int8=((iq_data/np.max(np.abs(iq_data)))*127).astype(np.int8)
        int8.tofile(f)
    
    iq_data = np.fromfile(open(inputFile), dtype=np.float32,offset = Offset*19)
    print(len(iq_data))
    int8=((iq_data/np.max(np.abs(iq_data)))*127).astype(np.int8)
    int8.tofile(f)



