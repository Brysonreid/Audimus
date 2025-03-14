import configparser
import datetime


#update new recording name
config = configparser.ConfigParser()
config.read('LimeSDRConf.ini')

Now = datetime.datetime.now()
NewName = "/home/pi/Audimus/Recordings/SDRdata" +Now.strftime('%Y-%m-%d-%H:%M:%S')
print(NewName)
config['Storage']['File']= NewName


with open('LimeSDRConf.ini', 'w') as configfile:
  config.write(configfile)

#delete recordings older than X days
print("Running Start.py")





