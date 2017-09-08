scan_sh_template = """#!/bin/sh
secs={}                         # Set interval (duration) in seconds.
endTime=$(( $(date +{}) + secs )) # Calculate end time.
while [ $(date +{}) -lt $endTime ]; do
iw dev wlan0 scan | awk -f wlan_scan_new.awk | grep {}
sleep {}
done"""

