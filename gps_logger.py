import csv
from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
from datetime import datetime
import time
import signal
import sys
import setgps10hz  ## sets ublox gps receiver to 10 hz

WRITE_FREQUENCY = 10

def signal_handler(signal, frame):
    print("Received Ctrl+C. Exiting.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_gps_data(gpsd_socket):
    while True:
        try:
            report = gpsd_socket.next()
            
            if report is not None and report['class'] == 'TPV':
                # Only consider TPV (Time, Position, Velocity) reports
                return report

        except StopIteration:
            # If there is no new data, wait for a short time
            time.sleep(0.01)  # 0.01 seconds (10 Hz)
        except KeyboardInterrupt:
            # Handle keyboard interrupt to stop the script
            break
        except Exception as e:
            print(f"Error in get_gps_data: {e}")

    return None  # Return None if no valid GPS data is obtained

def write_to_csv(data, writer):
    # Write GPS data to the CSV file
    writer.writerow({
        'timestamp': data.get('time', '') if 'time' in data else '',
        'latitude': data.get('lat', '') if 'lat' in data else '',
        'longitude': data.get('lon', '') if 'lon' in data else '',
        'altitude': data.get('alt', '') if 'alt' in data else '',
        'speed': data.get('speed', '')*2.236 if 'speed' in data else 0.0,  # m/s to mph
    })

def get_log_filename():
    # Create a filename based on the date and timestamp
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Log-{current_time}.csv"
    return filename

if __name__ == '__main__':
    try:
        log_filename = get_log_filename()

        with open(log_filename, 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'latitude', 'longitude', 'altitude', 'speed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header only if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()

            # Connect to the local gpsd
            gpsd_socket = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

            while True:
                gps_data = get_gps_data(gpsd_socket)
                if gps_data is not None:
                    print(f"Timestamp: {gps_data.get('time', '')}, Latitude: {gps_data.get('lat', '')}, Longitude: {gps_data.get('lon', '')}, Altitude: {gps_data.get('alt', '')}, Speed: {gps_data.get('speed', '')}")

                    write_to_csv(gps_data, writer)

                time.sleep(0.1)  # Record data at 10 Hz (0.1 seconds per loop)

    except KeyboardInterrupt:
        print("Script terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
