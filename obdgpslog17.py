#OBDGSPLOG17.py Written for MEGR3092 Fall 20017 by Mac McAlpine
#Based on obd-pi by Donour Sizemore and others
#IWANNAGOFAST2

#!/usr/bin/env python

import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time
import getpass
import RPi.GPIO as GPIO
import setgps10hz
import os
import numpy as np
import pygame
from pygame.locals import *
from sense_hat import SenseHat
from gpscontroller import *

startloggingonstartup = False #script will auto log on startup if true
blink = False #led blinker

loggingRate = 20	#sets logging rate delay

switchpin = 37# switch gpio input.  pulled down to activate
ledpin = 33 #led plus output
os.system('clear') #clear terminal, optional

pygame.init()

sense = SenseHat()
sense.show_message("LGR")


#while True:
#    for event in sense.stick.get_events():
#		if event.direction == "down":
#			loggingEnable = False
#		if event.direction == "up":
#			loggingEnable = True
        #print(event.direction, event.action)

setgps10hz.main()
print("starting GPSD")
sense.set_pixel(7, 0, [0, 255, 0])

os.system("gpsd /dev/ttyACM0") 
print("scanning for OBD serial")
from obd_utils import scanSerial

GPIO.setmode(GPIO.BOARD)
GPIO.setup(switchpin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(ledpin, GPIO.OUT) # LED output High = on
GPIO.output(ledpin, GPIO.LOW)

gpsc = GpsController()
gpsc.start()

def endMe():
	GPIO.remove_event_detect(switchpin)
	GPIO.cleanup()
	#gpsc.stopController()
	self.log_file.close
	sys.exit()


def doLogger():
	global loggingEnable
	for event in sense.stick.get_events(): #get joystick events
		#if GPIO.input(switchpin) or (event.action == 'pressed' and event.direction == "down"):
		if event.action == 'pressed' and event.direction == "down":
			print("Pin37 disengaged")
			print("Logging Disabled")
			GPIO.output(ledpin, GPIO.LOW)
			sense.set_pixel(0, 0, [255, 0, 0])
			loggingEnable = False
		#elif (not GPIO.input(switchpin)) or (event.action == 'pressed' and event.direction == "up"):
		elif event.action == 'pressed' and event.direction == "up": 
			print("Logging Enabled")
			GPIO.output(ledpin, GPIO.HIGH)
			loggingEnable = True
			sense.set_pixel(0, 0, [0, 255, 0])
		elif (event.action == 'pressed' and event.direction == "left"):
			endMe()

GPIO.add_event_detect(switchpin, GPIO.BOTH, callback=doLogger, bouncetime=300)



class OBD_Recorder():
    def __init__(self, path, log_items):
		self.port = None
		self.sensorlist = []
		localtime = time.localtime(time.time())
		filename = path+"car-"+str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".log"
		self.log_file = open(filename, "w", 128)
		#self.log_file.write("Time,RPM,MPH,Throttle,Load,Fuel Status\n");
		self.log_file.write("Time,RPM,MPH,Throttle,Load,Fuel Status,Latitude,Longitude,GPSTime,Altitude,GPSMPH,Track,Sats,AccX,AccY,AccZ,GyX,GyY,GyZ,PiT,PiP\n");

        
		for item in log_items:
			self.add_log_item(item)

		self.gear_ratios = [34/13, 39/21, 36/23, 27/20, 26/21, 25/22]
		#log_formatter = logging.Formatter('%(asctime)s.%(msecs).03d,%(message)s', "%H:%M:%S")

    def connect(self):
        portnames = scanSerial()
        #portnames = ['COM10']
        print portnames
        for port in portnames:
            self.port = obd_io.OBDPort(port, None, 2, 2)
            if(self.port.State == 0):
                self.port.close()
                self.port = None
            else:
                break

        if(self.port):
            print "Connected to "+self.port.port.name
            
    def is_connected(self):
        return self.port
        
    def add_log_item(self, item):
        for index, e in enumerate(obd_sensors.SENSORS):
            if(item == e.shortname):
                self.sensorlist.append(index)
                print "Logging item: "+e.name
                break
            
            
    def record_data(self):
        if(self.port is None):
            return None
        #print "logging " + str(datetime.now()) + " GPS Status:" + str(gpsc.fix.mode)

        #while 1:
        localtime = datetime.now()
        current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)+"."+str(localtime.microsecond)
        log_string = current_time
        results = {}
        for index in self.sensorlist:
                (name, value, unit) = self.port.sensor(index)
                log_string = log_string + ","+str(value)
                results[obd_sensors.SENSORS[index].shortname] = value;

		accelerometer_data = sense.get_accelerometer_raw()
		#gyroscope_data = sense.get_gyroscope_raw()
		#h = sense.get_humidity() 
		#p = sense.get_pressure()
		#t = sense.get_temperature_from_pressure() 
		
		gear = self.calculate_gear(results["rpm"], results["speed"])
		log_string = log_string #+ "," + str(gear) 
		log_string = log_string + "," + str(gpsc.fix.latitude)
		log_string = log_string + "," + str(gpsc.fix.longitude)
		log_string = log_string + "," + str(gpsc.utc)
		log_string = log_string + "," + str(gpsc.fix.altitude)
		#log_string = log_string + "," + str(gpsc.fix.time)
		log_string = log_string + "," + str(gpsc.fix.speed*2.237)
		log_string = log_string + "," + str(gpsc.fix.track)
		log_string = log_string + "," + str(len(gpsc.satellites))
		log_string = log_string + "," + str(accelerometer_data['x'])        
		log_string = log_string + "," + str(accelerometer_data['y'])
		log_string = log_string + "," + str(accelerometer_data['z'])
        #log_string = log_string + "," + str(gyroscope_data['x'])
        #log_string = log_string + "," + str(gyroscope_data['y'])
        #log_string = log_string + "," + str(gyroscope_data['z'])
        #str(sense.get_temperature_from_pressure())
        #str(sense.get_pressure())
        
        #print "GPS? ", str(gpsc.fix.mode) + "," + str(gpsc.utc) + "," + str(gpsc.fix.time)
        #log_string = log_string.fillna('') #replace NaN with no char
        self.log_file.write(log_string+"\n")

            
    def calculate_gear(self, rpm, speed):
        if speed == "" or speed == 0:
            return 0
        if rpm == "" or rpm == 0:
            return 0

        rps = rpm/60
        mps = (speed*1.609*1000)/3600
        
        primary_gear = 85/46 #street triple
        final_drive  = 47/16
        
        tyre_circumference = 1.978 #meters

        current_gear_ratio = (rps*tyre_circumference)/(mps*primary_gear*final_drive)
        
        #print current_gear_ratio
        gear = min((abs(current_gear_ratio - i), i) for i in self.gear_ratios)[1] 
        return gear
        
username = getpass.getuser()  
logitems = ["rpm", "speed", "throttle_pos", "load", "fuel_status"]
#o = OBD_Recorder('/home/'+username+'/pyobd-pi/log/', logitems) #had to hard code directory for auto run
o = OBD_Recorder('/home/pi/pyobd-pi/log/', logitems)
o.connect()

loggingEnable = startloggingonstartup

if loggingEnable:
	GPIO.output(ledpin, GPIO.HIGH)    	
	sense.set_pixel(7, 0, [0, 255, 0])
else:
	GPIO.output(ledpin, GPIO.LOW)
	sense.set_pixel(7, 0, [0, 0, 0])

sense.set_pixel(0, 0, [255, 0, 0])

while True:
	if loggingEnable:
		blink = not blink #recording light state
		if blink:
			sense.set_pixel(7, 0, [255, 0, 0])
		else:
			sense.set_pixel(7, 0, [0, 0, 0])
		#print "trying to log"
		#o.record_data()
		try:
			if not o.is_connected():
				print "Not connected"
				print "reconnecting"
				o.connect()
			time.sleep(1/loggingRate)
			o.record_data()
			print "logging " + str(datetime.now()) + " GStat:" + str(gpsc.fix.mode) + "GSpd:" +str(gpsc.fix.speed*2.237) + " GSats:" + str(len(gpsc.satellites))
			sense.set_pixel(0, 1, [0, 255, 0]) #set obd light to green
				
		except:
			if True:
				print "exception - likely no car/interface found"
				sense.set_pixel(0, 1, [255, 0, 0])	#set obd light to red		
                    #print "reconnecting"
                    #o.connect()
				time.sleep(.5);
	else:        
		#do this when not logging
		time.sleep(1)
		sense.set_pixel(7, 0, [0, 0, 0])	#turn off recording led
		print "idling " + str(datetime.now()) + " GStat:" + str(gpsc.fix.mode) + "GSpd:" +str(gpsc.fix.speed*2.237) + " GSats:" + str(len(gpsc.satellites))
	
	#usedsat = 0
	#for numsat in gpsc.satellites:
	#	if gpsc.satellites[numsat].used:
	#		usedsat=usedsat+1
	
	#print "usedsat " + str(usedsat)
	
		
	if str(gpsc.fix.mode) == "3":
		sense.set_pixel(1, 0, [0, 255, 0])
	elif str(gpsc.fix.mode) == "2":
		sense.set_pixel(1, 0, [0, 0, 255])
	else:
		sense.set_pixel(1, 0, [255, 0, 0])
		
	if (len(gpsc.satellites) > 11): 
		sense.set_pixel(2, 0, [0, 0, 255])
		sense.set_pixel(3, 0, [0, 0, 255])
		sense.set_pixel(4, 0, [0, 0, 255])
		sense.set_pixel(5, 0, [0, 0, 255])
	elif (len(gpsc.satellites) >5):
		sense.set_pixel(2, 0, [0, 0, 255])
		sense.set_pixel(3, 0, [0, 0, 255])
		sense.set_pixel(4, 0, [0, 0, 255])
		sense.set_pixel(5, 0, [0, 0, 0])
	elif (len(gpsc.satellites) >2):
		sense.set_pixel(2, 0, [0, 0, 255])
		sense.set_pixel(3, 0, [0, 0, 255])
		sense.set_pixel(4, 0, [0, 0, 0])
		sense.set_pixel(5, 0, [0, 0, 0])
	
	elif (len(gpsc.satellites) >0):
		sense.set_pixel(2, 0, [0, 0, 255])
		sense.set_pixel(3, 0, [0, 0, 0])
		sense.set_pixel(4, 0, [0, 0, 0])
		sense.set_pixel(5, 0, [0, 0, 0])
	elif (len(gpsc.satellites) ==0):
		sense.set_pixel(2, 0, [0, 0, 0])
		sense.set_pixel(3, 0, [0, 0, 0])
		sense.set_pixel(4, 0, [0, 0, 0])
		sense.set_pixel(5, 0, [0, 0, 0])
	doLogger()
	
