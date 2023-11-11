##Modified Sense Logger Example for MEGR3092
##measures sense hat sensors and GPS
#new comment

from datetime import datetime
from time import time
from select import select
from threading import Thread

from gps import *
import setgps10hz  ## sets ublox gps receiver to 10 hz
#from time import *

global gpsd

## Logging Settings
GPS_D=True
DELAY = 0
BASENAME = "Fall"
WRITE_FREQUENCY = 10
LOG_AT_START = True

def hello():
    print("MEGR3241 GPS only 10hz Logger")
    print("Press Ctrl-C to stop")


def file_setup(filename):
    header =[]
    header.append("MEGR3241_GPS_Logger_McLaren_Atlas_Compatible\ntime")
    
    ##header.extend(["time"])

    if GPS_D:    
        header.extend(["GPSmph","GPStrack","GPSlat","GPSlong","GPSalt","GPSsats"])
    with open(filename,"w") as f:
        f.write(",".join(str(value) for value in header)+ "\n")


## Function to collect data from the sense hat and build a string
def get_sense_data():
    localtime = datetime.now()
    ##current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)+"."+str(localtime.microsecond)
    current_time = str(datetime.now().time()) ## for simplified mega log viewer 
    ##current_time = time.time() ## for mclaren atlas
    log_string = current_time[:-3] ##strip last three time decimals to keep atlas happy

    sense_data=[]
    sense_data.append(log_string)  ##moved timestamp to beginning for megalogviewer compatability
    
    if GPS_D:
        gpsd.next()
        sense_data.append(gpsd.fix.speed*2.236)#m/s converted to mph
        sense_data.append(gpsd.fix.track)
        sense_data.append(gpsd.fix.latitude)
        sense_data.append(gpsd.fix.longitude)
        sense_data.append(gpsd.fix.altitude)
        #sense_data.append(gpsd.fix.sats)
        sense_data.append("sats")
        
        print ('speed (mph) ' , gpsd.fix.speed*2.236,"               \r"),
    return sense_data    


def show_state(logging):
    if logging:
        print("Logging on")
    else:
        print("Logging off")
        
    return logging_event,running

def log_data():
    output_string = ",".join(str(value) for value in sense_data)
    batch_data.append(output_string)

def timed_log():
    while run:
        if logging == True:
            log_data()
        time.sleep(DELAY)
        
## Main Program
hello()
setgps10hz.main() #sends command to GPS to force 10hz for ublox hardware

#global gpsd #bring it in scope
gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    
run=True
running = False
logging_event = True
logstate = False
logging=LOG_AT_START
#show_state(logging)
batch_data= []

#for new filenames each command
#filename = "log/"+"Log-"+str(datetime.now())+".csv"
#file_setup(filename)

if DELAY > 0:
    Thread(target= timed_log).start()

while run==True:
    ledrotate = 0;  
        
    sense_data = get_sense_data()
    #gpsd.next()  #get the latest GPS data from GPSD help with delays

    #logging_event, run = check_input()
    #logging_event = logging

    #logging_event,run = check_inputj() # causes a crash
    #logging_event = logging

    if logging_event and logging:
            logging = False
    
    elif logging_event :
            logging_event = False
            logging = True
            #for new file names each run
            localtime = time.localtime(time.time())
        
            filename = "Log-"+str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".csv"
            file_setup(filename)

    if logging == True and DELAY == 0:
        sense_data = get_sense_data()
        log_data()


    if len(batch_data) >= WRITE_FREQUENCY:
        with open(filename,"a") as f:
            for line in batch_data:
                f.write(line + "\n")
            batch_data = []
            
try:
    with open(filename,"a") as f:
        for line in batch_data:
                f.write(line + "\n")
                batch_data = []
                print(".")
except:
        print("No log file to close")
time.sleep(1)

