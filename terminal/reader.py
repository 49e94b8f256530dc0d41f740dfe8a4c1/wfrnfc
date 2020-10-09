import logging
import sys
from time import sleep

import coloredlogs
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG")

reader = SimpleMFRC522()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        logging.error("No terminal registration token specified")
        sys.exit(0)
    registration_token = sys.argv[1]
    logging.debug(f"Started terminal with registration token `{registration_token}`")
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
