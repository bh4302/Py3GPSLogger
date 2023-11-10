# Py3GPSLogger
Ublox USB GPS Data Logger for Use with Raspberry Pi 4 Running Python 3 Environment within Raspberry Pi OS x64
Code Created by Brayden Hill on 11/10/2023 for UNC Charlotte MEGR 3241: Advanced Motorsports Instrumentation

Materials Required:
1. Raspberry Pi 4 with Raspberry Pi OS x64 Installed
2. Ublox USB GPS
3. 2A Car Supply (USB Type C)

Installation Instructions:
First, update all required packages...
```python
sudo apt-get update
```
```python
sudo apt-get upgrade
```
```python
sudo apt-get autoremove
```
```python
sudo reboot
```
...then, install the required gspd-client packages/libraries...
```python
sudo apt-get install gpsd gpsd-clients
```
```python
pip install gpsd-py3 --break-system-packages
```
```python
sudo reboot
```
...now, clone the github code to your home directory...
```python
cd ~
```
```python
git clone https://github.com/bh4302/Py3GPSLogger.git
```
...and you now have the code installed!

Running Instructions:
To run the code and begin recording data, navigate to the directory where it was installed...
```python
cd Py3GPSLogger/
```
```python
python gps_logger_v2.py
```
...and use Ctrl^C to stop data recording.

Data will be automatically compiled into a .csv file with the recording timestamp, located in the same directory. 
