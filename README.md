pyobd
=====

<pre>Modification of pyobd and OBD-Pi with data logging centric features


Hardware Required:
1. Raspberry Pi 2/3 running raspbian stretch.  This is important as the script runs python version 2. The raspbian buster and newer will not work.
2. Ublox USB GPS 
4. 2A Car Supply / Switch or Micro USB Car Charger

pyOBD?

I took a fork of pyOBD’s software from their GitHub repository, https://github.com/peterh/pyobd, and used this as the basis for my program.
Note: For the following command line instructions, do not type the '#', that is only to indicate that it is a command to enter. 

Before proceeding, run:
#  sudo apt-get update
#  sudo apt-get upgrade
#  sudo apt-get autoremove
#  sudo reboot

Install these components using the command:
#  sudo apt-get install python-serial
#  sudo reboot 

Next, download the OBD-Pi Software direct from GitHub (https://github.com/Pbartek/pyobd-pi.git)

Or using the command:
#  cd ~
#  git clone https://github.com/macsboost/pyobd-pi.git

Vehicle Installation
The vehicle installation is quite simple.

1. Insert the USB Bluetooth dongle into the Raspberry Pi along with the SD card.

2. Insert the GPS to USB
To datalog run:

#  cd pyobd-pi
#  sudo su
#  python gpslogger3241mclaren.py

To exit the program just press Control and C or Alt and Esc.
/home/username/pyobd-pi/log/

Enjoy and drive safe!</pre>
