import configparser
import datetime
import numpy as np
import os


#Get updated time from time file
DateTimeFile = 'DateTime.txt'
TIME = str(np.loadtxt(DateTimeFile, dtype = str))
print(TIME)

newpath = "Recordings/" +TIME

#assuming a folder does not exist from this time
#if not os.path.exists(newpath):
    #os.makedirs(newpath)
#else:
    #pass


#update new recording name
config = configparser.ConfigParser()
config.read('LimeSDRConf.ini')

config['Storage']['folder'] = newpath


for I in range(1,6):
    NewName = newpath+'/Section'+str(I)
    try:
        check = config['Storage']['file'+str(I)]
        print("Checked")
    except:
        config['Storage']['file'+str(I)] = NewName
        print(NewName)

    with open('LimeSDRConf.ini', 'w') as configfile:
      config.write(configfile)

#delete recordings older than X days
print("Running Start.py")











