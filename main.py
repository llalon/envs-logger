import time
import serial
import logging
import settings
import csv

if (settings.ISS_ENABLED): 
    from ISStreamer.Streamer import Streamer
    # init isstreamer account
    streamer = Streamer(bucket_name=settings.BUCKET_NAME,
                    bucket_key=settings.BUCKET_KEY, access_key=settings.ACCESS_KEY)

# log file settings
logging.basicConfig(filename=settings.LOG_LOCATION, encoding='utf-8',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')


def log_message(msg):
    """ Prints msg to console and log file
    """
    if (settings.LOG_FILE_ENABLED):
        logging.info(msg)
    print(msg)


def log_data(temp, hum, data_path):
    """ Logs the inputed data to ISS and/or CSV 
    temp = temperature data (C)
    hum = humidity data (%)
    data_path = file path to save csv to
    """
    # Format the data
    temp = format(temp, ".2f")
    hum = format(hum, ".2f")

    # log to csv
    if (settings.CSV_ENABLED):
        log_message("Recording data to CSV...")

        with open(settings.CSV_LOCATION, mode='w') as file:
            data_csv = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_csv.writerow([temp, hum])

    # log to ISS
    if (settings.ISS_ENABLED):
        log_message("Sending data to server (ISS)...")

        streamer.log(settings.SENSOR_LOCATION_NAME +
                             " Temperature(C)", temp)
        streamer.log(settings.SENSOR_LOCATION_NAME +
                         " Humidity(%)", humidity)
        streamer.flush()

    return(0)


if __name__ == "__main__":
    log_message("starting envs-logger...")

    # Init serial port to read data from arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    # Set variables to NA (999.0)
    humidity = temperature = 999.0

    while True:
        try:
            # Read the data from the arduino
            log_message("Taking reading...")
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    humidity = float(line.split(' ')[1])
                    temperature = float(line.split(' ')[7])
                    log_message("Readin:: Hum: " +
                                str(humidity) + ", Temp: " + str(temperature))
                    log_message("done.")
                    break
                else:
                    pass
        except RuntimeError:
            log_message("RuntimeError, trying again...")
            continue

        # Record data if valid
        if (humidity != 999.0):
            log_message("Recording data...")

            # log data
            if (log_data(temperature, humidity) == 0):
                log_message("Data recorded successfully")
            else:
                log_message("Error: data unable to log")

        else:
            log_message("SerialError: 2, continuing")

        log_message("waiting for next read...")
        time.sleep(60 * settings.MINUTES_BETWEEN_READS)
