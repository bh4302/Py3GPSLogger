import csv
from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
from datetime import datetime
import time

def get_gps_data(gpsd_socket):
    while True:
        try:
            report = gpsd_socket.next()
            
            if report['class'] == 'TPV':
                # Only consider TPV (Time, Position, Velocity) reports
                return report

        except StopIteration:
            # If there is no new data, wait for a short time
            time.sleep(0.01)  # 0.01 seconds (10 Hz)
        except KeyboardInterrupt:
            # Handle keyboard interrupt to stop the script
            break
        except Exception as e:
            print(f"Error: {e}")

def write_to_csv(data, writer):
    # Write GPS data to the CSV file
    writer.writerow({
        'timestamp': data.get('time', ''),
        'latitude': data.get('lat', ''),
        'longitude': data.get('lon', ''),
        'altitude': data.get('alt', ''),
        'speed': data.get('speed', '')*2.236, #m/s converted to mph
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
                print(f"Timestamp: {gps_data.get('time')}, Latitude: {gps_data.get('lat')}, Longitude: {gps_data.get('lon')}, Altitude: {gps_data.get('alt')}, Speed: {gps_data.get('speed')}")

                write_to_csv(gps_data, writer)

                time.sleep(0.1)  # Record data at 10 Hz (0.1 seconds per loop)

    except KeyboardInterrupt:
        print("Script terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
