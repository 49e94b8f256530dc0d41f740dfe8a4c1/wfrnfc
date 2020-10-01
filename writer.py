import logging

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

reader = SimpleMFRC522()

if __name__ == '__main__':
    try:
            data = input('Write data:')
            logger.info(f"Hold a tag near the reader to write {data}")
            reader.write(data)
            logger.info("Write successful")
    finally:
            logger.debug("Cleanup GPIO")
            GPIO.cleanup()
