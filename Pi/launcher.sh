#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/Audimus

Pi_Temp=$(vcgencmd measure_temp)
echo "$Pi_Temp" >> pi_temp.log

# updating save file location name and deleting depricated files
sudo python Start.py

#start recording
sudo python LimeSDR_FM_Rx_Headless5.py

Pi_Temp=$(vcgencmd measure_temp)
echo "$Pi_Temp" >> pi_temp.log

cd /
