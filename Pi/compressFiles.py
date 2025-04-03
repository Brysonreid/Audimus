import numpy as np
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('LimeSDRConf.ini')
    
    inputFile = config['Storage']['file']
    output_filename =  config['Storage']['file']+"compressed"

    print(inputFile)
    
    Offset = 24000000



    



    with open(output_filename,"w") as f:
    
        for I in range(19):
        
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

    
    print("fileCompressed")

if __name__ =='__main__':
    main()

