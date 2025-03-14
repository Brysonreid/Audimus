# Audimus
Programing for Audimus SDR payload


This repository stores the programs used for the raspberry Pi planned to be used as part of the Audimus Cubesat mission to control the onboard SDR.

The raspberry Pi Zero 2W is running PiSDR v6.01 (Image obtained from https://github.com/luigifcruz/pisdr-image/releases) which comes with LimeSuite and GNUradio preinstalled.



The PC development environment can be set up through the following steps:

- Download the latest LimeSuite installation here: https://downloads.myriadrf.org/builds/PothosSDR/ 
- following the instructions on this page https://wiki.myriadrf.org/Lime_Suite
- Make sure to download the required windows drivers for the SDR indicated at the bottom of the page at the above link.
- This installation includes GNUradio and the appropriate packages for using the Lime SDR


GNURadio and LimeSuite are necessary for development of the SDR.


The "Pi" folder in this repository represents the current files present on the Pi board. 

- Launcher.sh is a shell script set to run on startup of the pi to initiate the scripts and actions the Pi should take during each pass.
    1. navigate to the Audimus directory on the Pi which holds all files
    2. get the temperature of the Pi and record it as a new entry in pi_temp.log
    3. run "Start.py" which creates a new sub directory/folder in /Recordings and updates the name of the recording files then deletes old files to maintain space on the driver
    4. run "LimeSDR_FM_Rx_Headless5.py" which initializes the SDR and begins taking data 
    5. exits to the root directory (at this point power will be turned off to the Pi)

Launcher.sh was setup through these instructions (https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/) and any errors with the script function will be logged in Logs/cronlog