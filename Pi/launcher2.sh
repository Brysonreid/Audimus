#!/bin/bash

echo "Running Start"

# Read current date and time
NOW=$(date +"%Y-%m-%d_%H-%M-%S")
NEW_PATH="/home/pi/Audimus/Recordings/Pass$NOW"

echo "$NEW_PATH"

# Create new recording directory if it does not exist
if [ ! -d "$NEW_PATH" ]; then
    mkdir -p "$NEW_PATH"
    echo "NewPath created"
fi

# Read list of files in the directory
FILES=($(ls "$NEW_PATH"))

declare -i recording_num
recording_num=$(sed -n '/^\[Storage\]/,/^\[/p' LimeSDRConf.ini | grep 'Recording_num' | sed 's/.*= *//')
echo "$recording_num"
# Loop through 1 to 5
for ((I=1; I<=recording_num; I++))
do
    FILENAME="Section$I"
    
    # Check if the file does not exist in the folder
    if [[ ! " ${FILES[@]} " =~ " $FILENAME " ]]; then
        NEW_NAME="$NEW_PATH/$FILENAME"
        
        # Update LimeSDRConf.ini (Assumes ini file format is simple key=value)
        sed -i "/^\[Storage\]/,/^\[/{s|^folder=.*|folder=$NEW_PATH|; s|^file=.*|file=$NEW_NAME|}" LimeSDRConf.ini
        FILE_VALUE=$(grep -A1 "\[Storage\]" LimeSDRConf.ini | grep "file=" | cut -d'=' -f2)
	echo "File path: $FILE_VALUE"
        # Run external scripts
        sudo python3 receive_data3.py
        sudo python3 compressFiles.py
    fi
done
