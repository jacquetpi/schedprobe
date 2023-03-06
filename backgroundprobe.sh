#!/bin/bash
if (( "$#" != "3" )) 
then
  echo "Missing argument : ./backgroundprobe.sh vmname delay output"
  exit -1
fi
loginctl enable-linger $( id -u -n )
mkdir -p ~/.config/systemd/user
vmname="$1"
delay="$2"
output="$3"
location=$( pwd )
cat misc/schedprobe.service | sed "s|#location#|$location|g" | sed "s|#vmname#|$vmname|g" | sed "s|#delay#|$delay|g" | sed "s|#output#|$output|g" > ~/.config/systemd/user/schedprobe.service
systemctl --user daemon-reload
systemctl --user start schedprobe
systemctl --user status schedprobe