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
    response = requests.get(f"{base_url}/api/v1/{registration_token}")
    if response.status_code == 404:
        logging.error("Terminal unknown")
        sys.exit(0)
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
