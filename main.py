from ISStreamer.Streamer import Streamer
import time
import serial
import logging
import settings

# --------- User Settings ---------
SENSOR_LOCATION_NAME = settings.SENSOR_LOCATION_NAME
BUCKET_NAME = settings.BUCKET_NAME
BUCKET_KEY = settings.BUCKET_KEY
ACCESS_KEY = settings.ACCESS_KEY
MINUTES_BETWEEN_READS = settings.MINUTES_BETWEEN_READS
METRIC_UNITS = settings.METRIC_UNITS
# ---------------------------------

# --------------DEBUG--------------
logging.basicConfig(filename = settings.LOG_LOCATION, encoding = 'utf-8', level = logging.DEBUG, format = '%(asctime)s %(message)s')
# ---------------------------------

# init isstreamer account
streamer = Streamer(bucket_name = BUCKET_NAME, bucket_key = BUCKET_KEY, access_key = ACCESS_KEY)

if __name__ == "__main__":

    logging.info("thlogger starting...")
    print("thlogger starting...")

    # Init serial port to read data from arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
    ser.flush()

    # Set variables to NA (999.0)
    humidity = temp_c = 999.0

    # bool to chck
    bool_snd = True

    while True:
        try:
            # Read the data from the arduino
            logging.info("Taking reading...")
            print("Taking reading...")

            while bool_snd:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    logging.info(line)
                    humidity = float(line.split(' ')[1])
                    temp_c = float(line.split(' ')[7])
                    logging.info("READIN:: Hum: " + str(humidity) + ", Temp: "+ str(temp_c))
                    logging.info("done.")
                    print("READIN:: Hum: " + str(humidity) + ", Temp: "+ str(temp_c))
                    print("done.")
                    bool_snd = False
                    break

                else:
                    #print("SerialError: 1, continuing...")
                    #logging.error("SerialError: 1, continuing...")
                    pass

        except RuntimeError:
            print("RuntimeError, trying again...")
            logging.error("RuntimeError, trying again...")
            continue

        # Only log the values if they arent NA
        if (humidity != 999.0):

            logging.info("Sending temperature to server...")
            print("Sending temperature to server...")

            # log temp
            if METRIC_UNITS:
                    streamer.log(SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)
            else:
                    temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
                    streamer.log(SENSOR_LOCATION_NAME + " Temperature(F)", temp_f)

            # log humidity
            print("Sending humidity to server...")
            logging.info("Sending humidity to server...")
            humidity = format(humidity,".2f")
            streamer.log(SENSOR_LOCATION_NAME + " Humidity(%)", humidity)
            streamer.flush()

            print("Writting to log")
            logging.info("Writting to log")

        else:
            logging.info("SerialError: 2, continuing")
            print("SerialError: 2, continuing")


        logging.info("Waiting for next read...")
        print("waiting for next read...")
        time.sleep(60 * MINUTES_BETWEEN_READS)
