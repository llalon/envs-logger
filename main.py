from ISStreamer.Streamer import Streamer
import time
import serial
import logging
import settings

# log file settings
logging.basicConfig(filename=settings.LOG_LOCATION, encoding='utf-8',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')


# init isstreamer account
streamer = Streamer(bucket_name=settings.BUCKET_NAME,
                    bucket_key=settings.BUCKET_KEY, access_key=settings.ACCESS_KEY)


def log_message(msg):
    """ Prints msg to console and log file
    """
    logging.info(msg)
    print(msg)


if __name__ == "__main__":

    log_message("starting envs-logger...")

    # Init serial port to read data from arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    # Set variables to NA (999.0)
    humidity = temp_c = 999.0

    while True:

        try:
            # Read the data from the arduino
            log_message("Taking reading...")
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    humidity = float(line.split(' ')[1])
                    temp_c = float(line.split(' ')[7])
                    log_message("READIN:: Hum: " +
                                str(humidity) + ", Temp: " + str(temp_c))
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

            # log temp
            if settings.METRIC_UNITS:
                streamer.log(settings.SENSOR_LOCATION_NAME +
                             " Temperature(C)", temp_c)
            else:
                temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
                streamer.log(settings.SENSOR_LOCATION_NAME +
                             " Temperature(F)", temp_f)

            # log humidity
            log_message("Sending humidity to server...")
            humidity = format(humidity, ".2f")
            streamer.log(settings.SENSOR_LOCATION_NAME +
                         " Humidity(%)", humidity)
            streamer.flush()

            log_message("Writting to log")

        else:
            log_message("SerialError: 2, continuing")

        log_message("waiting for next read...")
        time.sleep(60 * settings.MINUTES_BETWEEN_READS)
