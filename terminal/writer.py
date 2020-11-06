import logging

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

logger = logging.getLogger(__name__)

reader = SimpleMFRC522()


def write_tag(data):
    try:
        logger.info(f"Hold a tag near the terminal to write `{data}`")
        reader.write(data)
        logger.info("Write successful")
    finally:
        logger.debug("Cleanup GPIO")
        GPIO.cleanup()
