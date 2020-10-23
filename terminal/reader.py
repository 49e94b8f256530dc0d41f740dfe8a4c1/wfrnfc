import LCD
import logging
import os
import sys
from time import sleep

import coloredlogs
import requests
import RPi.GPIO as GPIO
from dotenv import find_dotenv, load_dotenv
from mfrc522 import SimpleMFRC522

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG")

reader = SimpleMFRC522()

load_dotenv(find_dotenv())

if __name__ == "__main__":
    base_url = f"http://{os.getenv('SERVER_HOST')}:{os.getenv('SERVER_PORT')}"
    logger.info(f"Using base_url `{base_url}`")
    if len(sys.argv) == 1:
        logging.error("No terminal registration token specified")
        sys.exit(0)
    registration_token = sys.argv[1]
    response = requests.get(f"{base_url}/api/v1/terminals/{registration_token}")
    if response.status_code == 404:
        logging.error("Terminal not found")
        sys.exit(0)
    logging.debug(f"Started terminal with registration token `{registration_token}`")
    lcd = LCD(2, 0x27, True)
    try:
        while True:
            logger.info("Hold a tag near the reader")
            lcd.message("WFRNFC RFID", 1)
            lcd.message("Access Control")
            id, data = reader.read()
            logger.info("Tag read successfully")
            logger.debug(f"id `{id}` data `{data}`")
            data = data.strip()
            response = requests.post(
                f"{base_url}/api/v1/tags/verify", data={"content": data}
            )
            if response.status_code == 200:
                logger.info("Authentication successful")
            else:
                logger.error("Authentication unsuccessful")
            sleep(3)
    except KeyboardInterrupt:
        logger.debug("Clear LCD")
        lcd.clear()
        logger.debug("Cleanup GPIO")
        GPIO.cleanup()
        raise
