from copy import Error
import logging

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from terminal.LCD import LCD

logger = logging.getLogger(__name__)

reader = SimpleMFRC522()
lcd = LCD(2, 0x27, True)


def write_tag(data):
    try:
        logger.info(f"Hold a tag near the terminal to write `{data}`")
        lcd.message("WFRNFC DEMO", 1)
        try:
            reader.write(data)
            logger.info("Write successful")
            lcd.message("Write successful", 2)
        except Exception as e:
            logger.error(e)
            lcd.message("Write unsuccessful", 2)
    finally:
        logger.debug("Cleanup GPIO")
        GPIO.cleanup()
