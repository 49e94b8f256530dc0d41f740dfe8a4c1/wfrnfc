import logging

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()


def write_tag(data):
    try:
        logger.info(f"Hold a tag near the reader to write `{data}`")
        reader.write(data)
        logger.info("Write successful")
    finally:
        logger.debug("Cleanup GPIO")
        GPIO.cleanup()
