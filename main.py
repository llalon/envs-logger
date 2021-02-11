import time
import serial
import logging
from influxdb import InfluxDBClient
import settings
import datetime

# log file settings
logging.basicConfig(filename=settings.LOG_LOCATION, encoding='utf-8',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')


def log_message(msg):
    """ Prints msg to console and log file
    """
    if (settings.LOG_FILE_ENABLED):
        logging.info(msg)
    print(msg)


def log_data(temp, hum):
    """ Logs the inputed data to Influx DB
    temp = temperature data (C)
    hum = humidity data (%)
    data_path = file path to save csv to
    """

    dt = datetime.datetime.utcnow()

    data = [
        {
            'measurement': settings.SENSOR_LOCATION_NAME,
            "time": dt,
            "fields": {
                "temperature": format(temp, ".2f"),
                "humidity": format(hum, ".2f")
            }
        }
    ]

    ifclient = InfluxDBClient(settings.INFLUXDB_IP, settings.INFLUXDB_PORT,
                              settings.INFLUXDB_USER, settings.INFLUXDB_PASS, settings.INFLUXDB_DB)
    if (ifclient.write_points(data)):
        return(0)

    return(1)


def main():
    log_message("starting envs-logger...")

    # Init serial port to read data from arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    # Set variables to NA (-999.0)
    humidity = temperature = -999.0

    while True:
        try:
            # Read the data from the arduino
            log_message("Taking reading...")
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    humidity = float(line.split(' ')[1])
                    temperature = float(line.split(' ')[7])
                    break
                else:
                    pass
        except RuntimeError:
            log_message("RuntimeError, trying again...")
            continue

        # Record data if valid
        if (humidity != -999.0):
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


if __name__ == "__main__":
    main()
