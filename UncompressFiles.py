import numpy as np
import os
import sys

output_folder = sys.argv[1]


if os.path.exists(output_folder):

    for output_filename in os.listdir(output_folder):
        print(output_filename)
        iq_data2 = np.fromfile(open(output_folder+"/"+output_filename), dtype=np.int8)
        float32=iq_data2.astype(np.int16)
        float32.tofile(output_folder+"/"+output_filename)
        
    print("Files Decompressed")
else:
    print(output_folder + " folder not found")