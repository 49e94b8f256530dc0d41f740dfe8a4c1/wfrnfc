import logging
import sys
from time import sleep

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

reader = SimpleMFRC522()

if __name__ == '__main__':
    try:
        while True:
            logger.info("Hold a tag near the reader")
            id, data = reader.read()
            logger.info(f"Id: {id} Data: {data}")
            sleep(3)
    except KeyboardInterrupt:
        logger.debug("Cleanup GPIO")
        GPIO.cleanup()
        raise
