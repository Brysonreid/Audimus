import numpy as np
import configparser
import os

def main():
    config = configparser.ConfigParser()
    config.read('LimeSDRConf.ini')
    
    inputFile = config['Storage']['file']
    output_filename =  config['Storage']['file']+"compressed"

    print(inputFile)
    
    Offset = 24000000
    size = os.path.getsize(inputFile)
    Sections = int(size/Offset)
    

    
    with open(output_filename,"w") as f:
    
        for I in range(Sections):
        
            print(I)
            with open(inputFile) as F:
                iq_data = np.fromfile(F, dtype=np.float32,count = int(Offset/4),offset = Offset*I)
            print(len(iq_data))
            int8=((iq_data/np.max(np.abs(iq_data)))*127).astype(np.int8)
            int8.tofile(f)
        
        with open(inputFile) as F:
            iq_data = np.fromfile(F, dtype=np.float32,count = int(Offset/4),offset = Offset*(I+1))
        int8=((iq_data/np.max(np.abs(iq_data)))*127).astype(np.int8)
        int8.tofile(f)

    
    if (os.path.getsize(output_filename) == (os.path.getsize(inputFile)/4)):
        os.remove(inputFile)
        print("Input File:"+str(inputFile)+" deleted")
    
    
    print("fileCompressed")

if __name__ =='__main__':
    main()

