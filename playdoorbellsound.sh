#!/bin/bash

# Sources: 
#  Play audio in background by adding defaults.pcm.card 1 (based on headphones interface in /proc/asound/cards) to /etc/asound.conf
#      https://raspberrypi.stackexchange.com/questions/120034/python-script-not-playing-audio-when-run-through-systemd
#  
#      sudo echo 'Environment=XDG_RUNTIME_DIR=/run/user/1000' >> /etc/systemd/system/doorcam.service 

ProcessAndPlayFile() {

	ffplay -nodisp $1 &> /dev/null &

	PID=$(pgrep ffplay)
	
	disown $PID

	sleep 25

	pkill -f ffplay
	#jobs | grep ffplay | cut -d']' -f 1 | cut -d'[' -f 2

}

BASEDIR=/home/pi/touchsensor

SOUNDSDIR="$BASEDIR/doorbellsounds"

SOUNDSDIRCONTENTS=$SOUNDSDIR/*

SOUNDSDIRCONTENTSARR=($SOUNDSDIRCONTENTS)

SOUNDSDIRCOUNT=${#SOUNDSDIRCONTENTSARR[@]}

SELECTION=$(( $RANDOM % $SOUNDSDIRCOUNT + 1 ))

ProcessAndPlayFile "${SOUNDSDIRCONTENTSARR[$SELECTION]}"
