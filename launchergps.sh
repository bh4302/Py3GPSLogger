#!/bin/sh
#launcher.sh
#navitate to home directory then to this directory then execute python script then home

cd /
cd home/pi/pyobd-pi

#sudo python obdlog.py
sudo python obdgpslog2.py > /dev/tty2
cd ~
