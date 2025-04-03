import configparser
import datetime
import numpy as np
import os
#import receive_data
import compressFiles
import time
#delete recordings older than X days
print("Running Start.py")


#update new recording name
config = configparser.ConfigParser()
config.read('LimeSDRConf.ini')


#Get updated time from time file
DateTimeFile = 'DateTime.txt'
TIME = str(np.loadtxt(DateTimeFile, dtype = str))

TIME = "Pass"+TIME


newpath = "Recordings/" +TIME

#assuming a folder does not exist from this time
if not os.path.exists(newpath):
    os.makedirs(newpath)
    print("NewPath")
else:
    pass


#update folder name in configfile
config['Storage']['folder'] = newpath

Files = os.listdir(newpath)
for I in range(1,6):
    
    Filename = 'Section'+str(I)
    
    if not Filename in Files:
        NewName = newpath+'/'+Filename
        config['Storage']['file'] = NewName
        
        with open('LimeSDRConf.ini', 'w') as configfile:
            config.write(configfile)
            
        #receive_data.main()
        #compressFiles.main()
        time.wait()
        print(NewName)
        




print(config['Storage']['folder'])

config['Storage']['file']







