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
sudo python receive_data.py

sudo python compressFiles.py

sudo python receive_data2.py

sudo python compressFiles.py


Pi_Temp=$(vcgencmd measure_temp)
echo "$Pi_Temp" >> pi_temp.log

sudo python compressFiles.py

cd /
