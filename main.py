import time
import serial
import logging
import settings

# log file settings
logging.basicConfig(filename=settings.LOG_LOCATION, encoding='utf-8',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')


def log_message(msg):
    """ Prints msg to console and log file
    """
    logging.info(msg)
    print(msg)


def log_data(temp, hum, data_path):
    """ Logs the inputed data to the csv
    temp = temperature data (C)
    hum = humidity data (%)
    data_path = file path to save csv to
    """

    temp = format(temp, ".2f")
    hum = format(hum, ".2f")

    # log to csv
    return(0)

    # Data not logged return 1
    log_message("ERROR: data unable to log")
    return(1)


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
                    log_message("READIN:: Hum: " +
                                str(humidity) + ", Temp: " + str(temperature))
                    log_message("done.")
                    break
                else:
                    pass
        except RuntimeError:
            log_message("RuntimeError, trying again...")
            continue

        # Send data to server. Only record if not NA
        if (humidity != 999.0):
            log_message("Sending temperature to server...")

            # log data
            log_data(temperature, humidity)

            log_message("Writting to log")

        else:
            log_message("SerialError: 2, continuing")

        log_message("waiting for next read...")
        time.sleep(60 * settings.MINUTES_BETWEEN_READS)
